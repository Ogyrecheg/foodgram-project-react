from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .views import CustomObtainAuthToken, Logout, Follow

urlpatterns = [
    path('', include('djoser.urls')),
    path('users/<id>/subscribe/', Follow.as_view()),
    path('auth/token/login/', CustomObtainAuthToken.as_view(), name='login'),
    path('auth/token/logout/', Logout.as_view(), name='logout'),
]
