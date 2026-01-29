from rest_framework import serializers
from loans.models import (
    Loan, LoanSchedule, LoanScheduleItem, LoanRateRevision, LoanAction
)

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = (
            "id", "name", "loan_type", "lender_name",
            "loan_account", "interest_type", "interest_frequency",
            "start_date", "original_principal", "is_active",
        )



class LoanScheduleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanScheduleItem
        fields = (
            "id", "emi_number", "due_date", "emi_amount",
            "principal_component", "interest_component",
            "outstanding_principal_after",
            "status", "payment_date",
        )

class LoanScheduleSerializer(serializers.ModelSerializer):
    items = LoanScheduleItemSerializer(many=True, read_only=True)

    class Meta:
        model = LoanSchedule
        fields = (
            "id", "interest_rate", "emi_amount",
            "start_emi_number", "start_date",
            "is_active", "items",
        )


class EmiPaySerializer(serializers.Serializer):
    bank_account = serializers.IntegerField()
    payment_date = serializers.DateField()

class RateChangeSerializer(serializers.Serializer):
    new_rate = serializers.DecimalField(max_digits=6, decimal_places=3)
    effective_date = serializers.DateField()
    keep_emi_fixed = serializers.BooleanField(default=True)

class PrepaymentSerializer(serializers.Serializer):
    bank_account = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    payment_date = serializers.DateField()

class TopUpSerializer(serializers.Serializer):
    bank_account = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)
    payment_date = serializers.DateField()
    new_rate = serializers.DecimalField(max_digits=6, decimal_places=3, required=False)
