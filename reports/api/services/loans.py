from django.db.models import Sum
from loans.models import LoanScheduleItem


def loan_interest_principal(user, start, end):
    qs = LoanScheduleItem.objects.filter(
        schedule__loan__created_by=user,
        status="PAID",
        payment_date__range=(start, end),
    )

    return {
        "principal_paid": qs.aggregate(
            Sum("principal_component")
        )["principal_component__sum"] or 0,

        "interest_paid": qs.aggregate(
            Sum("interest_component")
        )["interest_component__sum"] or 0,
    }
