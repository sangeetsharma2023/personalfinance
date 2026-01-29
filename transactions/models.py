from django.db import models
from core.models import BaseModel
from accounts.models import Account
from categories.models import Category
from django.db.models import Sum


class Transaction(BaseModel):
    TRANSACTION_TYPES = (
        ("EXPENSE", "Expense"),
        ("INCOME", "Income"),
        ("TRANSFER", "Transfer"),
        ("REVERSAL", "Reversal"),
    )

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    date = models.DateField()
    narration = models.CharField(max_length=255)
    is_draft = models.BooleanField(default=True)

    #Optional self-link for refunds/reversals
    reversed_transaction = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reversals",
    )

    def __str__(self):
        return f"{self.transaction_type} | {self.date} | {self.narration}"
    
    @property
    def total_amount(self):
        total = self.items.aggregate(
            s=Sum("amount")
        )["s"]
        return total or 0
    
    

    @property
    def display_amount(self):
        """
        Human-friendly amount for transaction list
        """
        if self.transaction_type == "TRANSFER":
            item = self.items.first()
            return item.amount if item else 0

        if self.transaction_type == "EXPENSE":
            return self.items.filter(is_debit=True).aggregate(
                s=Sum("amount")
            )["s"] or 0

        if self.transaction_type == "INCOME":
            return self.items.filter(is_debit=False).aggregate(
                s=Sum("amount")
            )["s"] or 0

        return 0

    @property
    def transfer_accounts(self):
        """
        Returns (from_account, to_account) for transfer
        """
        if self.transaction_type != "TRANSFER":
            return None, None

        dr = self.items.filter(is_debit=True).first()
        cr = self.items.filter(is_debit=False).first()

        return (
            dr.account if dr else None,
            cr.account if cr else None
        )

    @property
    def primary_account(self):
        """
        Account to display for Expense / Income
        """
        item = self.items.first()
        return item.account if item else None


    

# -------------------------
# TRANSACTION ITEM (DR / CR)
# -------------------------

class TransactionItem(BaseModel):
    transaction = models.ForeignKey(
        Transaction,
        related_name="items",
        on_delete=models.CASCADE,
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
    )

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    is_debit = models.BooleanField(help_text="True = Debit, False= Credit")

    def __str__(self):
        side = "DR" if self.is_debit else "CR"
        return f"{self.account.name} {side} {self.amount}"
    
# -------------------------
# TAG (CROSS-CUTTING DIMENSION)
# -------------------------

class Tag(BaseModel):
    """
    Generic tag for analytics.
    Examples:
    - Personal
    - Office
    - Medical
    - Travel
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
# -------------------------
# PERSON (WHO THE EXPENSE WAS FOR)
# -------------------------
class Person(BaseModel):
    """
    Represents a person for expense attribution.
    """
    name = models.CharField(max_length=100)
    relation = models.CharField(
        max_length=50,
        blank=True,
        help_text="e.g. Self, Spouse, Child",
    )

    def __str__(self):
        return self.name
    
# -------------------------
# EXPENSE ITEM (ITEM-WISE BREAKDOWN)
# -------------------------
class ExpenseItem(BaseModel):
    """
    Item-level breakdown of an expense transaction.
    """
    transaction_item = models.ForeignKey(
        TransactionItem,
        related_name="expense_items",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
    )

    description = models.CharField(max_length=255)

    amount = models.DecimalField(max_digits=14, decimal_places=2,)

    #Dimension : who the expense was for
    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    #Dimension: cross-cutting tags
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="expense_items",
        
    )

    def __str__(self):
        return f"{self.description} - {self.amount}"