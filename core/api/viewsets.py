from rest_framework.viewsets import ModelViewSet
from .mixins import OwnerCreateMixin
from .permissions import IsOwner

class OwnerModelViewSet(OwnerCreateMixin, ModelViewSet):
    permission_classes = [IsOwner]

    def get_queryset(self):
        return super().get_queryset().filter(
            created_by = self.request.user,
            is_deleted=False,
        )