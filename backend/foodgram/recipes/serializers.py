from rest_framework import serializers
import base64
from django.core.files.base import ContentFile

from .models import Recipes, Ingredients, IngredientsForRecipes, Tags, FavoriteRecipes, ShoppingCarts
from users.serializers import CustomFollowUserSerializer


class Base64ImageField(serializers.ImageField):
    """Кастомное поле под изображение."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)

        return super().to_internal_value(data)


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор модели тэгов."""

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


# class AddTagSerializer(serializers.ModelSerializer):
#     id = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True)
#
#     class Meta:
#         model = Tags
#         fields = ('id',)
#
#     def to_representation(self, instance):
#
#         return TagsSerializer(instance, context={'request': self.context.get('request')}).data


class ShowFavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор выдачи информации об избранном рецепте."""

    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов."""

    class Meta:
        model = FavoriteRecipes
        fields = ('user', 'recipe')

    def to_representation(self, instance):

        return ShowFavoriteRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class ShoppingCartsSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов из списка покупок."""

    class Meta:
        model = ShoppingCarts
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return ShowFavoriteRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    measurement_unit = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientsInRecipesSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов для рецепта."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientsForRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientsInRecipe(serializers.ModelSerializer):
    """Сериализатор додавления ингредиентов, их количества для конкретного рецепта."""

    id = serializers.IntegerField()
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
    """Сериализатор выдачи информации о рецепте."""

    author = CustomFollowUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagsSerializer(read_only=True, many=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField(read_only=True, default=False)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True, default=False)

    class Meta:
        model = Recipes
        fields = (
            'id', 'tags', 'image', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientsForRecipes.objects.filter(recipe=obj)

        return IngredientsInRecipesSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return FavoriteRecipes.objects.filter(user=request.user.id, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return ShoppingCarts.objects.filter(user=request.user.id, recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания/обновления рецепта."""

    tags = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all(), many=True)
    ingredients = AddIngredientsInRecipe(source='recipes_for_ingredients', many=True)
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()
    author = CustomFollowUserSerializer(read_only=True)

    class Meta:
        model = Recipes
        fields = ('tags', 'image', 'author', 'ingredients', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipes_for_ingredients')
        recipe = Recipes.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = Ingredients.objects.get(id=ingredient['id'])
            IngredientsForRecipes.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)

        instance.tags.clear()
        tags = validated_data.pop('tags')
        instance.tags.set(tags)

        instance.ingredients.clear()
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            current_ingredient = Ingredients.objects.get(id=ingredients['id'])
            IngredientsForRecipes.objects.create(
                recipe=instance,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )

        instance.save()

        return instance

    def to_representation(self, instance):
        return RecipesSerializer(instance).data
