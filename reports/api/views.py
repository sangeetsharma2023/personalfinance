from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reports.api.services.income_expense import (
    income_expense_summary,
    income_expense_periodic,
)
from reports.api.services.cashflow import cashflow_by_segment
from reports.api.services.loans import loan_interest_principal
from reports.api.services.investments import investment_flows
from reports.api.services.networth import net_worth

class IncomeExpenseReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = request.query_params["start"]
        end = request.query_params["end"]
        period = request.query_params.get("period", "MONTHLY")

        return Response({
            "summary": income_expense_summary(request.user, start, end),
            "periodic": income_expense_periodic(
                request.user, start, end, period
            ),
        })


class CashflowReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start = request.query_params["start"]
        end = request.query_params["end"]

        return Response(
            cashflow_by_segment(request.user, start, end)
        )

class NetWorthReport(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        as_on = request.query_params["as_on"]
        return Response(net_worth(request.user, as_on))
