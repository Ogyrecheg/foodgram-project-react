from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CustomObtainAuthToken, FavoriteAPIView, FollowView,
                    IngredientViewSet, Logout, RecipeViewSet,
                    ShoppingCartAPIView, TagViewSet, subscriptions)

router = SimpleRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('users/<id>/subscribe/', FollowView.as_view(), name='subscribe'),
    path('auth/token/login/', CustomObtainAuthToken.as_view(), name='login'),
    path('auth/token/logout/', Logout.as_view(), name='logout'),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    path('recipes/<id>/favorite/', FavoriteAPIView.as_view(), name='favorite'),
    path('recipes/<id>/shopping_cart/', ShoppingCartAPIView.as_view(), name='shopping_carts'),
]
