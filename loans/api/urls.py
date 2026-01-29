from rest_framework.routers import DefaultRouter
from loans.api.views import LoanViewSet

router = DefaultRouter()
router.register("", LoanViewSet, basename="loans")

urlpatterns = router.urls
