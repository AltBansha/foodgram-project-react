from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingList, Tag)
from .permissions import IsAdminOrSuperUser, IsAuthorOrReadOnly
from .serializers import (AddFavouriteRecipeSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShoppingListSerializer, TagSerializer)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny, ]
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user=user, recipe_id=OuterRef('pk')
                )
            ),
            is_in_shopping_cart=Exists(
                ShoppingList.objects.filter(
                    user=user, recipe_id=OuterRef('pk')
                )
            )
        )

    def get_permissions(self):
        if self.action == 'create':
            return IsAuthenticated(),
        if self.action in ['destroy', 'update', 'partial_update']:
            return IsAuthorOrReadOnly() and IsAdminOrSuperUser(),
        return AllowAny(),

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PUT'):
            return RecipeCreateSerializer

        return RecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class FavoriteViewSet(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = request.user
        data = {
            'user': user.id,
            'recipe': recipe_id,
        }
        serializer = AddFavouriteRecipeSerializer(
            data=data, context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        deleted_obj = Favorite.objects.filter(user=user,
                                              recipe=recipe).delete()
        if deleted_obj[0] == 0:
            return Response(
                'Такого рецепта нет в избранном.',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
        Favorite.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingVeiwSet(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = request.user
        data = {
            'user': user.id,
            'recipe': recipe_id,
        }
        context = {'request': request}
        serializer = ShoppingListSerializer(data=data, context=context)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        deleted_obj = ShoppingList.objects.filter(user=user,
                                                  recipe=recipe).delete()
        if deleted_obj[0] == 0:
            return Response(
                'Такого рецепта в списке покупок нет.',
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
        ShoppingList.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        users_shopping_list_recipes = user.user_shopping_lists.all()
        shopping_list = {}
        for record in users_shopping_list_recipes:
            recipe = record.recipe
            ingredients = IngredientAmount.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in shopping_list:
                    shopping_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    shopping_list[name]['amount'] += amount
        wishlist = ([f"{item} - {shopping_list[item]['amount']} "
                     f"{shopping_list[item]['measurement_unit']} \n "
                     for item in shopping_list])
        wishlist.append('\n')
        wishlist.append('FoodGram, 2021')
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
