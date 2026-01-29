from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.viewsets import OwnerModelViewSet
from investments.models import Investment, InvestmentHolding
from investments.api.serializers import (
    InvestmentSerializer,
    InvestmentHoldingSerializer,
)
from investments.api.services import (
    get_investment_cash_balance,
    get_portfolio_value,
)


class InvestmentViewSet(OwnerModelViewSet):
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer

    @action(detail=True, methods=["get"])
    def snapshot(self, request, pk=None):
        """
        Returns broker snapshot:
        cash + portfolio value.
        """
        investment = self.get_object()
        holdings = investment.holdings.all()

        cash = get_investment_cash_balance(
            investment.account
        )

        portfolio_value = get_portfolio_value(holdings)

        return Response({
            "investment": InvestmentSerializer(investment).data,
            "cash_balance": cash,
            "portfolio_value": portfolio_value,
            "net_value": cash + portfolio_value,
        })


class InvestmentHoldingViewSet(OwnerModelViewSet):
    queryset = InvestmentHolding.objects.all()
    serializer_class = InvestmentHoldingSerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            investment__created_by=self.request.user
        )
