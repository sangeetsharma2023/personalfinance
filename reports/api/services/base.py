from django.db.models.functions import TruncMonth, TruncQuarter, TruncYear
from django.db.models import Sum

PERIOD_TRUNC = {
    "MONTHLY": TruncMonth,
    "QUARTERLY": TruncQuarter,
    "YEARLY" : TruncYear,
}