from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.api.viewsets import OwnerModelViewSet
from loans.models import Loan
from loans.api.serializers import (
    LoanSerializer, LoanScheduleSerializer,
    EmiPaySerializer, RateChangeSerializer,
    PrepaymentSerializer, TopUpSerializer
)
from loans.api.services import (
    pay_emi, change_rate, part_prepay, top_up
)
from accounts.models import Account


class LoanViewSet(OwnerModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @action(detail=True, methods=["get"])
    def schedules(self, request, pk=None):
        loan = self.get_object()
        data = LoanScheduleSerializer(
            loan.schedules.order_by("-is_active", "start_emi_number"),
            many=True
        ).data
        return Response(data)

    @action(detail=True, methods=["post"])
    def pay_emi(self, request, pk=None):
        loan = self.get_object()
        s = EmiPaySerializer(data=request.data)
        s.is_valid(raise_exception=True)
        bank = Account.objects.get(id=s.validated_data["bank_account"])
        pay_emi(loan=loan, bank_account=bank, payment_date=s.validated_data["payment_date"])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def rate_change(self, request, pk=None):
        loan = self.get_object()
        s = RateChangeSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        change_rate(loan=loan, **s.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def part_prepay(self, request, pk=None):
        loan = self.get_object()
        s = PrepaymentSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        bank = Account.objects.get(id=s.validated_data["bank_account"])
        part_prepay(
            loan=loan, bank_account=bank,
            amount=s.validated_data["amount"],
            payment_date=s.validated_data["payment_date"],
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def top_up(self, request, pk=None):
        loan = self.get_object()
        s = TopUpSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        bank = Account.objects.get(id=s.validated_data["bank_account"])
        top_up(
            loan=loan, bank_account=bank,
            amount=s.validated_data["amount"],
            payment_date=s.validated_data["payment_date"],
            new_rate=s.validated_data.get("new_rate"),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
