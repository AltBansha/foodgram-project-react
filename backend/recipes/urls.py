from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCart, FavoriteViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingVeiwSet, TagViewSet)

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingVeiwSet.as_view()),
    path('recipes/<int:recipe_id>/favorite/', FavoriteViewSet.as_view()),
]
