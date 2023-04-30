from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from users.models import User


class Tag(models.Model):
    """Модель тэга."""

    name = models.CharField(
        max_length=200,
        verbose_name='название тэга',
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        verbose_name='color in Hex',
        unique=True,
        validators=[
            RegexValidator(
                regex='^[#](\w+){7}$',
                message='Неправильный формат HEX кода!'
            )
        ]
    )
    slug = models.SlugField(
        verbose_name='slug',
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        max_length=200,
        verbose_name='ингредиент',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единица измерения',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='uniq_name_and_measurement_unit'
            )
        ]
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""

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
        Ingredient,
        through='IngredientForRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
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

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    """Модель рецепт-ингредиент-количество."""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_for_recipe',
        verbose_name='id рецепта',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes_for_ingredients',
        verbose_name='id ингредиента',
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='uniq_recipe_and_ingredient'
            )
        ]
        ordering = ['id']
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецептов'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class FavoriteRecipe(models.Model):
    """Модель избранного рецепта."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chooser',
        verbose_name='Юзер',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='selected',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniq_user_and_recipe'
            )
        ]
        ordering = ['user']
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopper',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_recipes',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniq_recipe_and_user'
            )
        ]
        ordering = ['user']
        verbose_name = 'Рецепт для списка покупок'
        verbose_name_plural = 'Рецепты для списка покупок'

    def __str__(self):
        return f'{self.user} {self.recipe}'
