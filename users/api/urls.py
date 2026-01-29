from django.urls import path
from users.api.views import MeAPIView

urlpatterns = [
    path("me/", MeAPIView.as_view(), name="me"),
]
