from django.db import models
from core.models import BaseModel

class Account(BaseModel):
    """
    Represents a real world money container.
    """

    ACCOUNT_TYPES = (
        ("CASH", "Cash"),
        ("BANK", "Bank Account"),
        ("CREDIT_CARD", "Credit Card"),
        ("LOAN", "Loan Account"),
        ("INVESTMENT", "Investment Account"),
        ("SYSTEM_EXPENSE", "System Expense"),
        ("SYSTEM_INCOME", "System Income"),
        ("PERSONAL_LEDGER", "Personal Ledger"),
    )

    name = models.CharField(max_length=120)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES,)
    
    opening_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0,)

    opening_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.account_type})"