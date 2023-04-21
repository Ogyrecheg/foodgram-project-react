from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import RecipesViewSet, TagsViewSet, FavoriteAPIView, ShoppingCartsAPIView, IngredientsViewSet

router = SimpleRouter()
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<id>/favorite/', FavoriteAPIView.as_view(), name='favorite'),
    path('recipes/<id>/shopping_cart/', ShoppingCartsAPIView.as_view(), name='shopping_carts'),
]
