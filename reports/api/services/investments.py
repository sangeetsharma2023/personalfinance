from django.db.models import Sum
from transactions.models import TransactionItem


def investment_flows(user, start, end):
    qs = TransactionItem.objects.filter(
        transaction__created_by=user,
        transaction__is_draft=False,
        transaction__is_deleted=False,
        transaction__date__range=(start, end),
        account__account_type="INVESTMENT",
    )

    invested = qs.filter(is_debit=True).aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    liquidated = qs.filter(is_debit=False).aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    return {
        "invested": invested,
        "liquidated": liquidated,
        "net": invested - liquidated,
    }
