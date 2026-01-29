from django.urls import path
from reports.api.views import (
    IncomeExpenseReport,
    CashflowReport,
    NetWorthReport,
)



urlpatterns = [
    path("income-expense/", IncomeExpenseReport.as_view()),
    path("cashflow/", CashflowReport.as_view()),
    path("net-worth/", NetWorthReport.as_view()),
]
