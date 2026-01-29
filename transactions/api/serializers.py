from rest_framework import serializers
from transactions.models import (
    Transaction,
    TransactionItem,
    ExpenseItem,
)
from accounts.models import Account
from categories.models import Category
from transactions.models import Tag, Person


class ExpenseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseItem
        fields = (
            "id",
            "description",
            "category",
            "amount",
            "person",
            "tags",
        )


class TransactionItemSerializer(serializers.ModelSerializer):
    expense_items = ExpenseItemSerializer(many=True, read_only=True)

    class Meta:
        model = TransactionItem
        fields = (
            "id",
            "account",
            "amount",
            "is_debit",
            "expense_items",
        )
        read_only_fields = ("is_debit",)


class TransactionSerializer(serializers.ModelSerializer):
    items = TransactionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "id",
            "transaction_type",
            "date",
            "narration",
            "is_draft",
            "reversed_transaction",
            "items",
        )


class TransactionCreateSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(
        choices=Transaction.TRANSACTION_TYPES
    )
    date = serializers.DateField()
    narration = serializers.CharField()

    from_account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all()
    )
    to_account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all()
    )

    amount = serializers.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    expense_items = ExpenseItemSerializer(
        many=True,
        required=False,
    )
