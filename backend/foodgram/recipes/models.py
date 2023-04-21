from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tags(models.Model):
    """Тэги."""

    name = models.CharField(
        max_length=200,
        verbose_name='название тэга',
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        verbose_name='color in Hex',
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Ingredients(models.Model):
    """Ингредиенты."""

    name = models.CharField(
        max_length=200,
        verbose_name='ингредиенты',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единицы измерения',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipes(models.Model):
    """Рецепты."""

    name = models.CharField(
        max_length=200,
        verbose_name='название рецепта',
    )
    text = models.TextField(
        verbose_name='описание рецепта'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsForRecipes'
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='tags',
        verbose_name='Тэги',
    )
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='recipes/images/',
    )
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField(
        verbose_name='время публикации',
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientsForRecipes(models.Model):
    """Ингредиенты рецептов."""

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredients_for_recipe',
        verbose_name='id рецепта',
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        related_name='recipes_for_ingredients',
        verbose_name='id ингредиента',
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество',
    )

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'

    class Meta:
        ordering = ['id']
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'


class FavoriteRecipes(models.Model):
    """Избранные рецепты."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chooser',
        verbose_name='Юзер',
    )
    recipe = models.ForeignKey(
        Recipes,
        related_name='selected',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'{self.user} {self.recipe}'

    class Meta:
        ordering = ['user']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'


class ShoppingCarts(models.Model):
    """Список покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopper',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='shopping_recipes',
        verbose_name='Рецепт',
    )

    def __str__(self):
        return f'{self.user} {self.recipe}'

    class Meta:
        ordering = ['user']
        verbose_name = 'Рецепт для списка покупок'
        verbose_name_plural = 'Рецепты для списка покупок'
