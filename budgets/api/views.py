from rest_framework.decorators import action
from rest_framework.response import Response

from core.api.viewsets import OwnerModelViewSet
from budgets.models import Budget
from budgets.api.serializers import BudgetSerializer
from budgets.api.services import (
    calculate_budget_spent,
    calculate_allocation_spent,
)


class BudgetViewSet(OwnerModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        """
        Returns spent vs remaining for budget.
        """
        budget = self.get_object()
        spent = calculate_budget_spent(budget)

        return Response({
            "budget": BudgetSerializer(budget).data,
            "spent": spent,
            "remaining": budget.total_amount - spent,
        })

    @action(detail=True, methods=["get"])
    def allocations(self, request, pk=None):
        """
        Returns allocation-wise spent.
        """
        budget = self.get_object()
        data = []

        for alloc in budget.allocations.all():
            spent = calculate_allocation_spent(alloc)
            data.append({
                "category": alloc.category.name,
                "allocated": alloc.amount,
                "spent": spent,
                "remaining": alloc.amount - spent,
            })

        return Response(data)
