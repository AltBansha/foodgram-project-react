import django_filters as filters

from .models import Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name="tags__slug", method='filter_tags')
    author = filters.CharFilter(
        field_name="author__slug",
        method='filter_author'
    )
    is_favorited = filters.CharFilter(
        field_name="is_favorited__slug",
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.CharFilter(
        field_name="is_in_shopping_cart__slug",
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter_tags(self, queryset, name, tags):
        return queryset.filter(tags__slug__in=tags.split(','))

    def filter_author(self, queryset, name, author):
        return queryset.filter(author__slug__in=author.split(','))

    def filter_is_favorited(self, queryset, name, is_favorited):
        return queryset.filter(is_favorited__slug__in=is_favorited.split(','))

    def filter_is_in_shopping_cart(self, queryset, name, is_in_shopping_cart):
        return queryset.filter(
            is_in_shopping_cart__slug__in=is_in_shopping_cart.split(',')
        )
