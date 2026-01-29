from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import date

from reports.api.services.networth import net_worth
from reports.api.services.income_expense import income_expense_summary, income_expense_periodic
from reports.api.services.cashflow import cashflow_by_segment

@login_required
def index(request):
    today = date.today()
    start_of_year = date(today.year, 1, 1)

    networth_data = net_worth(request.user, today)

    income_expense = income_expense_summary(
        request.user,
        start_of_year,
        today
    )

    monthly = income_expense_periodic(
        request.user,
        start_of_year,
        today,
        period="MONTHLY"
    )

    cashflow = cashflow_by_segment(
        request.user,
        start_of_year,
        today
    )

    context = {
        "networth": networth_data["net_worth"],
        "income": income_expense["income"],
        "expense": income_expense["expense"],
        "net": income_expense["net"],
        "monthly": monthly,
        "cashflow": cashflow,
    }

    return render(request, "dashboard/index.html", context)
