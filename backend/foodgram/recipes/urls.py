from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import RecipesViewSet, TagsViewSet, FavoriteAPIView

router = SimpleRouter()
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<id>/favorite/', FavoriteAPIView.as_view(), name='favorite'),
]
