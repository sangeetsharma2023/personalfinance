from django.db.models import Sum
from accounts.models import Account
from transactions.models import TransactionItem


def net_worth(user, as_on):
    accounts = Account.objects.filter(
        created_by=user,
        is_deleted=False,
    )

    result = []
    total = 0

    for acc in accounts:
        dr = TransactionItem.objects.filter(
            account=acc,
            is_debit=True,
            transaction__date__lte=as_on,
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        cr = TransactionItem.objects.filter(
            account=acc,
            is_debit=False,
            transaction__date__lte=as_on,
        ).aggregate(Sum("amount"))["amount__sum"] or 0

        bal = dr - cr
        total += bal

        result.append({
            "account": acc.name,
            "type": acc.account_type,
            "balance": bal,
        })

    return {
        "accounts": result,
        "net_worth": total,
    }
