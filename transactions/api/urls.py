from django.urls import path
from rest_framework.routers import DefaultRouter
from transactions.api.views import (
    TransactionViewSet,
    TransactionCreateAPIView,
)

router = DefaultRouter()
router.register("", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("create/", TransactionCreateAPIView.as_view()),
] + router.urls
