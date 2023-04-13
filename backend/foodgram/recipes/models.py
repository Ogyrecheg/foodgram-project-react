from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Tags(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=7,
        verbose_name='color in Hex',
        blank=True,
    )
    slug = models.SlugField(max_length=200)


class Ingredients(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)


class Recipes(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(Ingredients, through='IngredientsForRecipes')
    tags = models.ManyToManyField(Tags, related_name='tags', verbose_name='Тэги')
    image = models.ImageField(
        upload_to='recipes/images/',
    )
    cooking_time = models.PositiveIntegerField(validators=[MinValueValidator(1)])


class IngredientsForRecipes(models.Model):
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
        verbose_name='количество',
    )


class FavoriteRecipes(models.Model):
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
