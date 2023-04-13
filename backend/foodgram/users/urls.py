from django.urls import path, include

from .views import CustomObtainAuthToken, Logout, FollowView, subscriptions

urlpatterns = [
    path('users/subscriptions/', subscriptions, name='hello'),
    path('', include('djoser.urls')),
    path('users/<id>/subscribe/', FollowView.as_view()),
    path('auth/token/login/', CustomObtainAuthToken.as_view(), name='login'),
    path('auth/token/logout/', Logout.as_view(), name='logout'),
]
