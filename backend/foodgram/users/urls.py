from django.urls import path, include
from djoser.views import UserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenBlacklistView

from .views import CustomTokenObtainPairView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('auth/token/logout/', TokenBlacklistView.as_view(), name='logout'),
]
