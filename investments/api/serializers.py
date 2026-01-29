from rest_framework import serializers
from investments.models import Investment, InvestmentHolding
from accounts.models import Account

class InvestmentSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(
        source="account.name",
        read_only=True,
    )

    class Meta:
        model = Investment
        fields = (
            "id",
            "name",
            "investment_type",
            "identifier",
            "account",
            "account_name",
            "notes",
        )


class InvestmentHoldingSerializer(serializers.ModelSerializer):
    investment_name = serializers.CharField(
        source="investment.name",
        read_only=True,
    )

    market_value = serializers.SerializerMethodField()

    class Meta:
        model = InvestmentHolding
        fields = (
            "id",
            "investment",
            "investment_name",
            "date",
            "quantity",
            "price",
            "market_value",
        )

    def get_market_value(self, obj):
        return obj.quantity * obj.price
