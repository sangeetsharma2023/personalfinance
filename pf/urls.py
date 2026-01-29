from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import EmailTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("ui.urls")),


    # JWT Auth
    path("api/auth/login/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("api/users/", include("users.api.urls")),

    path("api/accounts/", include("accounts.api.urls")),

    path("api/transactions/", include("transactions.api.urls")),

    path("api/categories/", include("categories.api.urls")),

    path("api/budgets/", include("budgets.api.urls")),

    path("api/investments/", include("investments.api.urls")),

    path("api/loans/", include("loans.api.urls")),

    path("api/reports/", include("reports.api.urls")),

]
