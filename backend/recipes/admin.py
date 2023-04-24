from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientForRecipe, Recipe,
                     ShoppingCart, Tag)


class TagInLine(admin.TabularInline):
    model = Recipe.tags.through


class IngredientInLine(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'text',
        'author',
        'favorite',

    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    inlines = [TagInLine, IngredientInLine]

    def favorite(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()


@admin.register(IngredientForRecipe)
class IngredientForRecipe(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = ('recipe',)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user',)
