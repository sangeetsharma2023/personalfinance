from django.contrib import admin
from .models import Budget, BudgetAllocation


# -------------------------
# INLINE: BUDGET ALLOCATIONS
# -------------------------
class BudgetAllocationInline(admin.TabularInline):
    model = BudgetAllocation
    extra = 1


# -------------------------
# BUDGET ADMIN
# -------------------------
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "amount",
        "period_type",
        "start_date",
        "end_date",
        "is_active",
        "allocated_amount",
        "unallocated_amount",
    )

    list_filter = (
        "period_type",
        "is_active",
    )

    search_fields = ("name",)

    inlines = [BudgetAllocationInline]

    filter_horizontal = ("tags",)


# -------------------------
# ALLOCATION ADMIN (OPTIONAL)
# -------------------------
@admin.register(BudgetAllocation)
class BudgetAllocationAdmin(admin.ModelAdmin):
    list_display = (
        "budget",
        "category",
        "amount",
    )

    list_filter = ("budget",)
