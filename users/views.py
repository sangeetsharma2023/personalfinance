from rest_framework_simplejwt.views import TokenObtainPairView
from .auth import EmailTokenObtainPairSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
