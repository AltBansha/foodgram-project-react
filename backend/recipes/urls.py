from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCart, FavoriteAPIView, IngredientViewSet,
                    RecipeViewSet, ShoppingVeiwSet, TagViewSet)

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')


urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view(),
         name='download_shopping_cart'),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingVeiwSet.as_view(),
         name='add_recipe_to_shopping_cart'),
    path('recipes/<int:recipe_id>/favorite/', FavoriteAPIView.as_view(),
         name='add_recipe_to_favorite'),
]
