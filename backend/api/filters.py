import django_filters
from rest_framework import filters

from recipes.models import Recipe, Tag


class CustomIngredientFilter(filters.SearchFilter):
    search_param = "name"


class CustomRecipeFilter(django_filters.FilterSet):
    tags = django_filters.rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.rest_framework.BooleanFilter(
        method='is_favorited_func',
    )
    is_in_shopping_cart = django_filters.rest_framework.BooleanFilter(
        method='is_in_shopping_cart_func'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def is_favorited_func(self, queryset, name, value):
        if value:

            return queryset.filter(selected__user=self.request.user)

        return queryset

    def is_in_shopping_cart_func(self, queryset, name, value):
        if value:

            return queryset.filter(shopping_recipes__user=self.request.user)

        return queryset
