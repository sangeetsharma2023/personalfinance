from django.db import transaction as db_tx
from loans.models import Loan, LoanSchedule, LoanScheduleItem, LoanRateRevision, LoanAction
from accounts.models import Account
from transactions.api.services import create_transaction_service
from decimal import Decimal


def _active_schedule(loan):
    return loan.schedules.filter(is_active=True).first()

def _last_paid_item(schedule):
    return schedule.items.filter(status="PAID").order_by("-emi_number").first()

def _next_unpaid_item(schedule):
    return schedule.items.filter(status="UNPAID").order_by("emi_number").first()

def _outstanding_after_last_paid(schedule):
    last_paid = _last_paid_item(schedule)
    if last_paid:
        return last_paid.outstanding_principal_after
    # cut-over case: derive from opening balance via account
    return Decimal("0.00")


@db_tx.atomic
def pay_emi(*, loan: Loan, bank_account: Account, payment_date):
    schedule = _active_schedule(loan)
    item = _next_unpaid_item(schedule)
    if not item:
        raise ValueError("No unpaid EMI")

    create_transaction_service(
        user=loan.created_by,
        transaction_type="EXPENSE",
        date=payment_date,
        narration=f"EMI #{item.emi_number} - {loan.name}",
        from_account=bank_account,
        to_account=loan.loan_account,
        amount=item.emi_amount,
    )

    item.status = "PAID"
    item.payment_date = payment_date
    item.save(update_fields=["status", "payment_date"])

    LoanAction.objects.create(
        loan=loan,
        action_type="EMI_PAYMENT",
        action_date=payment_date,
        amount=item.emi_amount,
        created_by=loan.created_by,
    )


@db_tx.atomic
def change_rate(*, loan: Loan, new_rate, effective_date, keep_emi_fixed=True):
    schedule = _active_schedule(loan)
    last_paid = _last_paid_item(schedule)
    outstanding = _outstanding_after_last_paid(schedule)

    LoanRateRevision.objects.create(
        loan=loan,
        old_rate=schedule.interest_rate,
        new_rate=new_rate,
        effective_date=effective_date,
        created_by=loan.created_by,
    )

    schedule.is_active = False
    schedule.save(update_fields=["is_active"])

    # NOTE: schedule generation math intentionally abstracted
    new_schedule = LoanSchedule.objects.create(
        loan=loan,
        interest_rate=new_rate,
        emi_amount=schedule.emi_amount,  # default keep EMI
        start_emi_number=(last_paid.emi_number + 1) if last_paid else 1,
        start_date=effective_date,
        is_active=True,
        created_by=loan.created_by,
    )

    LoanAction.objects.create(
        loan=loan,
        action_type="RATE_CHANGE",
        action_date=effective_date,
        notes="EMI fixed" if keep_emi_fixed else "Tenure fixed",
        created_by=loan.created_by,
    )

    return new_schedule


@db_tx.atomic
def part_prepay(*, loan: Loan, bank_account: Account, amount, payment_date):
    schedule = _active_schedule(loan)

    create_transaction_service(
        user=loan.created_by,
        transaction_type="EXPENSE",
        date=payment_date,
        narration=f"Part prepayment - {loan.name}",
        from_account=bank_account,
        to_account=loan.loan_account,
        amount=amount,
    )

    schedule.is_active = False
    schedule.save(update_fields=["is_active"])

    LoanAction.objects.create(
        loan=loan,
        action_type="PART_PREPAYMENT",
        action_date=payment_date,
        amount=amount,
        created_by=loan.created_by,
    )


@db_tx.atomic
def top_up(*, loan: Loan, bank_account: Account, amount, payment_date, new_rate=None):
    create_transaction_service(
        user=loan.created_by,
        transaction_type="INCOME",
        date=payment_date,
        narration=f"Top-up - {loan.name}",
        from_account=loan.loan_account,
        to_account=bank_account,
        amount=amount,
    )

    schedule = _active_schedule(loan)
    schedule.is_active = False
    schedule.save(update_fields=["is_active"])

    LoanAction.objects.create(
        loan=loan,
        action_type="TOP_UP",
        action_date=payment_date,
        amount=amount,
        created_by=loan.created_by,
    )
