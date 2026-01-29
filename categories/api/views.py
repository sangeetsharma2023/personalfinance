from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.viewsets import OwnerModelViewSet
from categories.models import Category
from categories.api.serializers import (
    CategorySerializer,
    CategoryTreeSerializer,
)

class CategoryViewSet(OwnerModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        return super().get_queryset().filter(
            is_active=True
        )

    @action(detail=False, methods=["get"])
    def tree(self, request):
        """
        Returns hierarchical category tree.
        """
        roots = Category.objects.filter(
            parent__isnull=True,
            is_active=True,
            is_deleted=False,
            created_by=request.user,
        )
        serializer = CategoryTreeSerializer(roots, many=True)
        return Response(serializer.data)
