from rest_framework import serializers
from budgets.models import Budget, BudgetAllocation

class BudgetAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetAllocation
        fields = (
            "id",
            "category",
            "amount",
        )


class BudgetSerializer(serializers.ModelSerializer):
    allocations = BudgetAllocationSerializer(
        many=True,
        read_only=True,
    )

    allocated_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        read_only=True,
    )

    unallocated_amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = Budget
        fields = (
            "id",
            "name",
            "total_amount",
            "period_type",
            "start_date",
            "end_date",
            "category",
            "person",
            "tags",
            "is_active",
            "allocated_amount",
            "unallocated_amount",
            "allocations",
        )
