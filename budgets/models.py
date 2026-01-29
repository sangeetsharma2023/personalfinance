from django.db import models
from core.models import BaseModel
from categories.models import Category
from transactions.models import Tag, Person

class Budget(BaseModel):
    """
    Defines a spending limit over a time period.
    """
    PERIOD_TYPES = (
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
        ("CUSTOM", "Custom"),
    )

    name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=14, decimal_places=2,)

    period_type = models.CharField(max_length=10, choices=PERIOD_TYPES)

    start_date = models.DateField()
    end_date = models.DateField()

    #--- Dimensions (all optional, but at least one required logically)

    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text="Applies to this category (including subcategories)",

    )

    person = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        help_text="Optional tags this budget applies to",      
        
    )

    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    @property
    def allocated_amount(self):
        """
        Docstring for allocated_amount
        
        :Sum of all child allocations.
        """
        return sum(
            a.amount for a in self.allocations.all()
        )
    
    @property
    def unallocated_amount(self):
        """
        Docstring for unallocated_amount
        
        :Flexible amount not tied to any allocations.
        """
        return self.total_amount - self.allocated_amount
    

# ==================================
# BUDGET ALLOCATION (SUB-LIMITS)
# ==================================
class BudgetAllocation(BaseModel):
    """
    Docstring for BudgetAllocation
    Defines sub-limits inside a parent budget.
    These are SOFT limits.
    """

    budget = models.ForeignKey(
        Budget,
        related_name="allocations",
        on_delete=models.CASCADE,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        help_text="Specific sub-category this allocation applies to",
    )

    amount = models.DecimalField(max_digits=14, decimal_places=2,
                                 help_text="Allocated amount within the parent budget",)

    class Meta:
        unique_together = ("budget", "category")

    def __str__(self):
        return f"{self.category.name} → {self.amount}"