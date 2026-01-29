from django.db import models
from core.models import BaseModel
from accounts.models import Account

class Loan(BaseModel):
    
    LOAN_TYPES = (
        ("HOME", "Home"),
        ("PERSONAL", "Personal"),
        ("CAR", "Car Loan"),
        ("EDUCATION", "Education Loan"),
        ("OTHER", "Other"),
    )

    INTEREST_TYPES = (
        ("FIXED", "Fixed"),
        ("FLOATING", "Floating"),
    )

    INTEREST_FREQUENCY =(
        ("MONTHLY", "Monthly"),
        ("DAILY", "Daily"),
    )

    name = models.CharField(max_length=150)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)

    lender_name = models.CharField(max_length=150)

    loan_account = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        limit_choices_to={"account_type": "LOAN"},
        related_name="loan",
    )

    interest_type = models.CharField(
        max_length=10,
        choices=INTEREST_TYPES,
    )

    interest_frequency = models.CharField(
        max_length=10,
        choices=INTEREST_FREQUENCY,
        default="MONTHLY",
    )

    start_date = models.DateField()
    original_principal = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class LoanRateRevision(BaseModel):
    loan = models.ForeignKey(
        Loan,
        related_name="rate_revisions",
        on_delete=models.CASCADE,
    )

    old_rate = models.DecimalField(
        max_digits=6,
        decimal_places=3,
    )

    new_rate = models.DecimalField(
        max_digits=6,
        decimal_places=3,
    )

    effictive_date = models.DateField()

    reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Bank rate revision, repo change etc."
    )

    def __str__(self):
        return f"{self.loan.name}: {self.old_rate}% → {self.new_rate}%"
    
class LoanSchedule(BaseModel):
    """
    Represents a repayment plan version.
    Only ONE schedule is active at a time.
    """

    loan = models.ForeignKey(
        Loan,
        related_name="schedules",
        on_delete=models.CASCADE,
    )

    interest_rate = models.DecimalField(
        max_digits=6,
        decimal_places=3,
    )

    emi_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    start_emi_number = models.PositiveIntegerField()
    start_date = models.DateField()

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.loan.name} | EMI from #{self.start_emi_number}"



class LoanScheduleItem(BaseModel):
    """
    One EMI row.
    NEVER recalculated once PAID.
    """

    STATUS = (
        ("UNPAID", "Unpaid"),
        ("PAID", "Paid"),
    )

    schedule = models.ForeignKey(
        LoanSchedule,
        related_name="items",
        on_delete=models.CASCADE,
    )

    emi_number = models.PositiveIntegerField()
    due_date = models.DateField()

    emi_amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    principal_component = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    interest_component = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    outstanding_principal_after = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default="UNPAID",
    )

    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"EMI #{self.emi_number} ({self.status})"


class LoanAction(BaseModel):
    """
    Event log for all loan-related actions.
    """

    ACTION_TYPES = (
        ("DISBURSEMENT", "Disbursement"),
        ("EMI_PAYMENT", "EMI Payment"),
        ("RATE_CHANGE", "Interest Rate Change"),
        ("PART_PREPAYMENT", "Part Prepayment"),
        ("FULL_PREPAYMENT", "Full Prepayment"),
        ("TOP_UP", "Top-up Loan"),
    )

    loan = models.ForeignKey(
        Loan,
        related_name="actions",
        on_delete=models.CASCADE,
    )

    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
    )

    action_date = models.DateField()

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        null=True,
        blank=True,
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.loan.name} | {self.action_type}"
