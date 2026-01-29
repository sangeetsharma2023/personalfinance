from rest_framework.routers import DefaultRouter
from budgets.api.views import BudgetViewSet

router = DefaultRouter()
router.register("", BudgetViewSet, basename="budgets")

urlpatterns = router.urls
