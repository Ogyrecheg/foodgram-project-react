from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CustomRecipeFilter
from .models import Recipes, Tags, FavoriteRecipes, ShoppingCarts, IngredientsForRecipes, Ingredients
from .permissions import OwnerOrAdmin
from .serializers import (
    RecipesSerializer, TagsSerializer, FavoriteRecipesSerializer,
    ShoppingCartsSerializer, RecipeCreateSerializer, IngredientsSerializer
)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тэгов."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipes.objects.all()
    permission_classes = (OwnerOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilter

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':

            return (AllowAny(),)

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':

            return RecipesSerializer

        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        serializer_class=RecipesSerializer
    )
    def download_shopping_cart(self, request):
        """Функция выдачи ингредиентов из списка покупок. """

        ingredients_for_show = 'Ваши ингредиенты: '

        ingredients = IngredientsForRecipes.objects.filter(
            recipe__shopping_recipes__user=request.user
        ).order_by(
            'ingredient__name'
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            amount=Sum('amount')
        )

        for ingredient in ingredients:
            ingredients_for_show += (
                f"\n{ingredient['ingredient__name']}"
                f" {ingredient['amount']}"
                f" {ingredient['ingredient__measurement_unit']}"
            )

        return HttpResponse(ingredients_for_show, content_type='application')


class FavoriteAPIView(APIView):
    """Вью-класс на добавление/удаление рецепта в/из избранное(ого)."""

    def post(self, request, id):
        user_id = request.user.id
        recipe_id = id
        data = {'user': user_id, 'recipe': recipe_id}
        serializer = FavoriteRecipesSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user_id = request.user.id
        recipe_id = id
        selected_bundle = FavoriteRecipes.objects.filter(user=user_id, recipe=recipe_id)

        if not selected_bundle.exists():

            return Response('Данный рецепт не находится в избранном!', status=status.HTTP_400_BAD_REQUEST)

        selected_bundle.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartsAPIView(APIView):
    """Вью-класс на добавление/удаление рецепта в/из список(а) покупок."""

    def post(self, request, id):
        user_id = request.user.id
        recipe_id = id
        data = {'user': user_id, 'recipe': recipe_id}
        serializer = ShoppingCartsSerializer(data=data, context={'request': request})

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user_id = request.user.id
        recipe_id = id
        selected_bundle = ShoppingCarts.objects.filter(user=user_id, recipe=recipe_id)

        if not selected_bundle.exists():

            return Response('Данный рецепт не находится в cписке покупок!', status=status.HTTP_400_BAD_REQUEST)

        selected_bundle.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
