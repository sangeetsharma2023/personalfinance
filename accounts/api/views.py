from core.api.viewsets import OwnerModelViewSet
from accounts.models import Account
from accounts.api.serializers import AccountSerializer


class AccountViewSet(OwnerModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer