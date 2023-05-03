from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (FavoriteRecipe, Ingredient, IngredientForRecipe,
                            Recipe, ShoppingCart, Tag)
from users.models import Follow, User

from .filters import CustomIngredientFilter, CustomRecipeFilter
from .pagination import CustomUserPagination
from .permissions import OwnerOrAdmin
from .serializers import (CustomAuthTokenSerializer, FavoriteRecipeSerializer,
                          FollowSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubscriptionsSerializer,
                          TagSerializer)


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        content = {'auth_token': token.key}

        return Response(content, status=status.HTTP_201_CREATED)


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowView(APIView):
    def post(self, request, id):
        data = {'user': request.user.id, 'author': id}
        serializer = FollowSerializer(data=data, context={'request': request}
                                      )
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        follow = Follow.objects.filter(user=request.user.id, author=id)

        if not follow.exists():

            return Response(
                'Вы не подписаны на данного автора!',
                status=status.HTTP_400_BAD_REQUEST
            )

        follow.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([OwnerOrAdmin])
def subscriptions(request):
    follows = User.objects.filter(author__user=request.user)
    paginator = CustomUserPagination()
    result = paginator.paginate_queryset(follows, request, view=None)

    serializer = SubscriptionsSerializer(
        result,
        many=True,
        context={'request': request},
    )

    return paginator.get_paginated_response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для тэгов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (CustomIngredientFilter,)
    search_fields = ('name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilter

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':

            return (AllowAny(),)

        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':

            return RecipeSerializer

        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        serializer_class=RecipeSerializer
    )
    def download_shopping_cart(self, request):
        """Функция выдачи ингредиентов из списка покупок. """

        ingredients_for_show = 'Ваши ингредиенты: '

        ingredients = IngredientForRecipe.objects.filter(
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
                f'\n{ingredient["ingredient__name"]}'
                f' {ingredient["amount"]}'
                f' {ingredient["ingredient__measurement_unit"]}'
            )

        return HttpResponse(ingredients_for_show, content_type='application')


class FavoriteAPIView(APIView):
    """Вью-класс на добавление/удаление рецепта в/из избранное(ого)."""

    def post(self, request, id):
        data = {'user': request.user.id, 'recipe': id}
        serializer = FavoriteRecipeSerializer(
            data=data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        selected_bundle = FavoriteRecipe.objects.filter(
            user=request.user.id,
            recipe=id
        )

        if not selected_bundle.exists():

            return Response(
                'Данный рецепт не находится в избранном!',
                status=status.HTTP_400_BAD_REQUEST
            )

        selected_bundle.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartAPIView(APIView):
    """Вью-класс на добавление/удаление рецепта в/из список(а) покупок."""

    def post(self, request, id):
        data = {'user': request.user.id, 'recipe': id}
        serializer = ShoppingCartSerializer(
            data=data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        selected_bundle = ShoppingCart.objects.filter(
            user=request.user.id,
            recipe=id,
        )

        if not selected_bundle.exists():

            return Response(
                'Данный рецепт не находится в cписке покупок!',
                status=status.HTTP_400_BAD_REQUEST
            )

        selected_bundle.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
