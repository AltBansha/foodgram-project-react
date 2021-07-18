from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    FollowAPIView,
    FavoriteViewSet,
    ShoppingVeiwSet,
    DownloadShoppingCart,
    showfollows,
)


router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')
# router.register(
#     r'shoppinglists', ShoppingListAPIView, basename='shoppinglists'
# )
router.register(r'tags', TagViewSet, basename='tags')
# router.register(r'subscriptions', ShowFollowList)


urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('', include(router.urls)),
    path('', include('users.urls')),
    path('users/subscriptions/', showfollows),
    path('users/<int:user_id>/subscribe/', FollowAPIView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingVeiwSet.as_view()),
    path('recipes/<int:recipe_id>/favorite/', FavoriteViewSet.as_view()),
]
