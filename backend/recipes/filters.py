import django_filters as filters

from .models import Ingredient, Recipe


class RecipeFilter(filters.FilterSet):
    tags = filters.CharFilter(field_name="tags__slug", method='filter_tags')
    author = filters.CharFilter(
        field_name="author__slug",
        method='filter_author'
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_tags(self, queryset, name, tags):
        return queryset.filter(tags__slug__in=tags.split(','))

    def filter_author(self, queryset, name, author):
        return queryset.filter(author__slug__in=author.split(','))

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return Recipe.objects.filter(favorites__user=user)
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.username
        if value:
            return Recipe.objects.filter(user_shopping_lists__user=user)
        return Recipe.objects.all()


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name', )
