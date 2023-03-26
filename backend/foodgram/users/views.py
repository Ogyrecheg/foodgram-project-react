from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import CustomUserSerializer, CustomTokenObtainPairSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
