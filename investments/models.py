from django.db import models
from core.models import BaseModel
from accounts.models import Account

class Investment(BaseModel):
    INVESTMENT_TYPES = (
        ("EQUITY", "Equity / Stock"),
        ("MUTUAL_FUND", "Mutual"),
        ("FIXED_INCOME", "Fixed Income"),
        ("CRYPTO", "Crypto"),
        ("OTHER", "Other"),
    )

    name = models.CharField(max_length=120)
    investment_type = models.CharField(
        max_length=20,
        choices=INVESTMENT_TYPES,
    )

    #Each investment is linked to ONE investment account
    account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        limit_choices_to={"account_type": "INVESTMENT"},
    )

    identifier = models.CharField(
        max_length=50,
        blank=True,
        help_text="ISIN / Ticker / Scheme Code",
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class InvestmentHolding(BaseModel):
    investment = models.ForeignKey(
        Investment,
        related_name="holdings",
        on_delete=models.CASCADE,
    )

    date = models.DateField()

    quantity = models.DecimalField(max_digits=18, decimal_places=6,)

    price = models.DecimalField(max_digits=14, decimal_places=4, help_text="Price per unit")

    def __str__(self):
        return f"{self.investment.name} {self.quantity}"