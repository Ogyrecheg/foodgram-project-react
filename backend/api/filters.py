import django_filters

from recipes.models import Recipe, Tag


class CustomRecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = django_filters.BooleanFilter(
        method='is_favorited_func',
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='is_in_shopping_cart_func'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def is_favorited_func(self, queryset, name, value):
        if value:

            return queryset.filter(selected=self.request.user)

        return queryset

    def is_in_shopping_cart_func(self, queryset, name, value):
        if value:

            return queryset.filter(shopping_cart__user=self.request.user)

        return queryset
