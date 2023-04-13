from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipes, Tags, FavoriteRecipes
from .serializers import RecipesSerializer, TagsSerializer, FavoriteRecipesSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteAPIView(APIView):
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
