from django.contrib import admin
from .models import (
    Transaction,
    TransactionItem,
    ExpenseItem,
    Tag,
    Person,
)


# -------------------------
# INLINE: EXPENSE ITEMS
# -------------------------
class ExpenseItemInline(admin.TabularInline):
    model = ExpenseItem
    extra = 1


# -------------------------
# INLINE: TRANSACTION ITEMS
# -------------------------
class TransactionItemInline(admin.TabularInline):
    model = TransactionItem
    extra = 1
    show_change_link = True


# -------------------------
# TRANSACTION ADMIN
# -------------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "transaction_type",
        "narration",
        "is_draft",
    )

    list_filter = (
        "transaction_type",
        "is_draft",
        "date",
    )

    search_fields = ("narration",)
    inlines = [TransactionItemInline]


# -------------------------
# TRANSACTION ITEM ADMIN
# -------------------------
@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = (
        "transaction",
        "account",
        "amount",
        "is_debit",
    )

    inlines = [ExpenseItemInline]


# -------------------------
# SUPPORTING MODELS
# -------------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name", "relation")
    search_fields = ("name",)
