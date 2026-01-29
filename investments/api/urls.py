from rest_framework.routers import DefaultRouter
from investments.api.views import (
    InvestmentViewSet,
    InvestmentHoldingViewSet,
)

router = DefaultRouter()
router.register("", InvestmentViewSet, basename="investments")
router.register("holdings", InvestmentHoldingViewSet, basename="investment-holdings")

urlpatterns = router.urls
