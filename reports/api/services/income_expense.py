from django.db.models import Sum
from transactions.models import TransactionItem
from .base import PERIOD_TRUNC

def income_expense_summary(user, start, end):
    qs = TransactionItem.objects.filter(
        transaction__created_by=user,
        transaction__is_draft=False,
        transaction__is_deleted = False,
        transaction__date__range=(start,end),
    )

    income = qs.filter(
        is_debit = False,
        account__account_type="SYSTEM_INCOME",
    ).aggregate(total=Sum("amount"))["total"] or 0

    expense = qs.filter(
        is_debit=True,
        account__account_type="SYSTEM_EXPENSE",
    ).aggregate(total=Sum("amount"))["total"] or 0

    return {
        "income": income,
        "expense": expense,
        "net": income-expense,
    }

def income_expense_periodic(user, start, end, period):
    trunc = PERIOD_TRUNC[period]

    qs = TransactionItem.objects.filter(
        transaction__created_by=user,
        transaction__is_draft=False,
        transaction__is_deleted=False,
        transaction__date__range=(start, end),
    ).annotate(p=trunc("transaction__date"))

    data = qs.values("p", "account__account_type").annotate(
        total=Sum("amount")
    )

    result = {}
    for row in data:
        p = row["p"]
        result.setdefault(p, {"income": 0, "expense": 0})

        if row["account__account_type"] == "SYSTEM_INCOME":
            result[p]["income"] += row["total"]
        elif row["account__account_type"] == "SYSTEM_EXPENSE":
            result[p]["expense"] += row["total"]

    return [
        {
            "period": k,
            "income": v["income"],
            "expense": v["expense"],
            "net": v["income"] - v["expense"],
            "drilldown": {
                "start": k,
                "end": k,
            }
        }
        for k, v in sorted(result.items())
    ]
