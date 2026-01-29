from django.db.models import Sum
from transactions.models import TransactionItem


def get_investment_cash_balance(account):
    """
    Returns broker cash balance from transactions.
    """
    debit = TransactionItem.objects.filter(
        account=account,
        is_debit=True,
        transaction__is_deleted=False,
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    credit = TransactionItem.objects.filter(
        account=account,
        is_debit=False,
        transaction__is_deleted=False,
    ).aggregate(Sum("amount"))["amount__sum"] or 0

    return debit - credit


def get_portfolio_value(holdings):
    return sum(
        h.quantity * h.price for h in holdings
    )
