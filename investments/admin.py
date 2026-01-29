from django.contrib import admin
from .models import Investment, InvestmentHolding


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ("name", "investment_type", "account")
    search_fields = ("name", "identifier")


@admin.register(InvestmentHolding)
class InvestmentHoldingAdmin(admin.ModelAdmin):
    list_display = ("investment", "date", "quantity", "price")
    list_filter = ("investment",)
