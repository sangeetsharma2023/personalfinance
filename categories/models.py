from django.db import models

from core.models import BaseModel

class Category(BaseModel):
    """
    Expense/ Income classification.
    """

    CATEGORY_TYPES = (
        ("EXPENSE", "Expense"),
        ("INCOME", "Income"),
    )

    name = models.CharField(max_length=120)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    parent = models.ForeignKey(
        "self",
        null = True,
        blank = True,
        related_name="children",
        on_delete=models.PROTECT,
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name