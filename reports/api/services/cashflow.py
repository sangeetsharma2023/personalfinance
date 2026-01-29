from django.db.models import Sum
from transactions.models import TransactionItem


def cashflow_by_segment(user, start, end):
    qs = TransactionItem.objects.filter(
        transaction__created_by=user,
        transaction__is_draft=False,
        transaction__is_deleted=False,
        transaction__date__range=(start, end),
    )

    def balance(account_type):
        dr = qs.filter(
            is_debit=True,
            account__account_type=account_type
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        cr = qs.filter(
            is_debit=False,
            account__account_type=account_type
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        return dr - cr

    return {
        "operating": {
            "income_expense": balance("SYSTEM_INCOME") - balance("SYSTEM_EXPENSE")
        },
        "loans": {
            "principal_paid": balance("LOAN")
        },
        "investments": {
            "net_flow": balance("INVESTMENT")
        },
        "informal": {
            "personal_ledgers": balance("PERSONAL_LEDGER")
        },
        "net_cashflow": (
            balance("SYSTEM_INCOME")
            - balance("SYSTEM_EXPENSE")
            + balance("LOAN")
            + balance("INVESTMENT")
        ),
    }
