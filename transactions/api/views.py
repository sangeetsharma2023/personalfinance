from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.api.viewsets import OwnerModelViewSet
from transactions.models import Transaction
from transactions.api.serializers import (
    TransactionSerializer,
    TransactionCreateSerializer,
)
from transactions.api.services import create_transaction_service

class TransactionViewSet(OwnerModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionCreateAPIView(APIView):
    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tx = create_transaction_service(
            user=request.user,
            **serializer.validated_data
        )

        return Response(
            TransactionSerializer(tx).data,
            status=status.HTTP_201_CREATED,
        )
