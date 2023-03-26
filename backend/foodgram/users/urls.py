from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CustomTokenObtainPairView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/login/', CustomTokenObtainPairView.as_view(), name='login'),
]
