from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.models import F

from .models import Recipes, Ingredients, IngredientsForRecipes, Tags, FavoriteRecipes
from users.serializers import CustomFollowUserSerializer


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class AddTagSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all())

    class Meta:
        model = Tags
        fields = ('id',)

    def to_representation(self, instance):

        return TagsSerializer(instance, context={'request': self.context.get('request')}).data


class ShowFavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipes
        fields = ('user', 'recipe')

    def to_representation(self, instance):

        return ShowFavoriteRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class IngredientsSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientsInRecipesSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsForRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientsInRecipe(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredients.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientsForRecipes
        fields = ('id', 'amount')

    def to_representation(self, instance):
        serializer = IngredientsInRecipesSerializer(
            instance,
            context={'request': self.context.get('request')}
        )

        return serializer.data


class RecipesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
    author = CustomFollowUserSerializer(read_only=True)
    ingredients = AddIngredientsInRecipe(many=True, required=False)
    tags = AddTagSerializer(read_only=True, many=True, required=False)
    is_favorited = serializers.SerializerMethodField(read_only=True, default=False)

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        recipe = Recipes.objects.create(**validated_data)

        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)

        return recipe

    def get_is_favorited(self, obj):
        request = self.context.get('request')

        return FavoriteRecipes.objects.filter(user=request.user.id, recipe=obj).exists()
