import base64
import re

from django.contrib.auth import authenticate
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSerializer

from recipes.models import (FavoriteRecipe, Ingredient, IngredientForRecipe,
                            Recipe, ShoppingCart, Tag)
from users.models import Follow, User


class CustomUserSerializer(UserCreateSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=150, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')

    def validate_username(self, username):
        if not re.match(r'^[a-zA-Z0-9-_]+$', username):
            raise serializers.ValidationError('Недопустимые символы username.')

        return username


class CustomFollowUserSerializer(CustomUserSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    is_subscribed = serializers.SerializerMethodField(default=False, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return Follow.objects.filter(user=request.user.id, author=obj).exists()


class SubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        return Follow.objects.filter(user=request.user.id, author=obj).exists()


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.EMAIL_FIELD


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_('Email'),
        write_only=True
    )
    password = serializers.CharField(
        label=_('Password'),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author')

    def to_representation(self, instance):

        return CustomFollowUserSerializer(instance.author, context={'request': self.context.get('request')}).data

    def validate(self, data):
        if Follow.objects.filter(
                user=data['user'],
                author=data['author'],
        ):
            raise serializers.ValidationError('Ошибка подписки: Вы уже подписаны на данного пользователя!')

        if data['user'] == data['author']:
            raise serializers.ValidationError('Ошибка подписки: нельзя подписаться сам на себя !')

        return data


class Base64ImageField(serializers.ImageField):
    """Кастомное поле под изображение."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='image.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тэга."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class ShowFavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор выдачи информации об избранном рецепте."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор избранного рецепта."""

    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return ShowFavoriteRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data

    def validate(self, data):
        if FavoriteRecipe.objects.filter(
                user=data['user'],
                recipe=data['recipe'],
        ):
            raise serializers.ValidationError('Вы уже добавили в избранное данный рецепт!')

        return data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов из списка покупок."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        return ShowFavoriteRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data

    def validate(self, data):
        if ShoppingCart.objects.filter(
                user=data['user'],
                recipe=data['recipe'],
        ):
            raise serializers.ValidationError('Вы уже добавили в cписок покупок данный рецепт!')

        return data


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    measurement_unit = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента для рецепта."""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientInRecipe(serializers.ModelSerializer):
    """Сериализатор додавления ингредиента, его количества для конкретного рецепта."""

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'amount')

    def to_representation(self, instance):
        serializer = IngredientInRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        )

        return serializer.data


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор выдачи информации о рецепте."""

    author = CustomFollowUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField(required=False, allow_null=True)
    is_favorited = serializers.SerializerMethodField(read_only=True, default=False)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True, default=False)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'image', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'text', 'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = IngredientForRecipe.objects.filter(recipe=obj)

        return IngredientInRecipeSerializer(ingredients, many=True).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return FavoriteRecipe.objects.filter(user=request.user.id, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return ShoppingCart.objects.filter(user=request.user.id, recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания/обновления рецепта."""

    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    ingredients = AddIngredientInRecipe(source='recipes_for_ingredients', many=True)
    cooking_time = serializers.IntegerField()
    image = Base64ImageField()
    author = CustomFollowUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'tags', 'image', 'author',
            'ingredients', 'name', 'text', 'cooking_time'
        )

    def validated_text(self, value):
        if len(value) > 200:
            raise serializers.ValidationError(
                'Описание рецепта не должно быть больше 200 символов'
            )

    def validated_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                'Значение времени приготовления рецепта должно быть больше либо равно 1')

        return value

    @staticmethod
    def make_ingredient_for_recipe_obj(ingredients, recipe):
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(id=ingredient['id'])
            IngredientForRecipe.objects.create(
                recipe=recipe,
                ingredient=current_ingredient,
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipes_for_ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self.make_ingredient_for_recipe_obj(ingredients, recipe)

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
        ingredients = validated_data.pop('recipes_for_ingredients')

        self.make_ingredient_for_recipe_obj(ingredients, instance)

        instance.save()

        return instance

    def to_representation(self, instance):
        return RecipeSerializer(instance).data
