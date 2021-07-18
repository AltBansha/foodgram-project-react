from django.contrib import admin

from .models import Favorite, Follow, Ingredient, Recipe, ShoppingList, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'amount',
        'measurement_unit'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class IngredientsInline(admin.TabularInline):
    model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'ingredients',
        'is_favorited_count',
    )

    def is_favorited_count(self, obj):
        return obj.is_favorited.all().count()
    is_favorited_count.short_description = 'Количество сохранений'

    def ingredients(self, obj):
        return list(obj.ingredient.all())
    ingredients.short_description = 'Ингредиенты'

    search_fields = ('name', 'author__username',)
    empty_value_display = '-пусто-'


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'recipe',
    )
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    empty_value_display = '-пусто-'


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'purchase',
    )
    empty_value_display = '-пусто-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(Favorite, FavoriteAdmin)
