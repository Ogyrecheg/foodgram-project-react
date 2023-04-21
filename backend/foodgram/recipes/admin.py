from django.contrib import admin

from .models import (Tags, Ingredients, Recipes, IngredientsForRecipes,
                     FavoriteRecipes, ShoppingCarts)


class TagsInLine(admin.TabularInline):
    model = Recipes.tags.through


class IngredientsInLine(admin.TabularInline):
    model = Recipes.ingredients.through


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name',)


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
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
    inlines = [TagsInLine, IngredientsInLine]

    def favorite(self, obj):
        return FavoriteRecipes.objects.filter(recipe=obj).count()


@admin.register(IngredientsForRecipes)
class IngredientsForRecipes(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = ('recipe',)


@admin.register(FavoriteRecipes)
class FavoriteRecipesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user',)


@admin.register(ShoppingCarts)
class ShoppingCartsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    search_fields = ('user',)
