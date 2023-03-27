from django.urls import path, include

from .views import LogOutView, TokenObtainPairView


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token/logout/', LogOutView.as_view(), name='logout'),
]
