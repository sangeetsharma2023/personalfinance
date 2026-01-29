from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.api.serializers import UserSerializer


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def __str__(self,request):
        return Response(UserSerializer(request.user).data)