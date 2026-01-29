from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "opening_balance", "opening_date", "is_active")
    list_filter = ("account_type", "is_active")