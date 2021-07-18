from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from users.models import CustomUser

from .filters import RecipeFilter
from .models import Favorite, Follow, Ingredient, Recipe, ShoppingList, Tag
from .permissions import IsAdminOrSuperUser, IsAuthorOrReadOnly
from .serializers import (AddFavouriteRecipeSerializer, IngredientSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          ShowFollowersSerializer, TagSerializer,
                          UserFollowSerializer)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrSuperUser]
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        if self.request.query_params:
            queryset = Ingredient.objects.filter(
                name__istartswith=self.request.query_params.get('search'),
                amount=1)
        else:
            queryset = Ingredient.objects.all()
        return queryset


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend, ]
    filter_class = RecipeFilter

    def get_permissions(self):
        if self.action == 'create':
            return IsAuthenticated(),
        if self.action in ['destroy', 'update', 'partial_update']:
            return IsAuthorOrReadOnly() and IsAdminOrSuperUser(),
        return AllowAny(),

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RecipeCreateSerializer
        if self.request.method == 'PUT':
            return RecipeCreateSerializer
        else:
            return RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, user_id):
        user = self.request.user
        author = get_object_or_404(CustomUser, id=user_id)
        if user == author:
            return Response(
                'Нельзя подписаться на себя',
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(user=user, author=author).exists():
            return Response(
                'Вы уже подписались',
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.create(user=user, author=author)
        serializer = ShowFollowersSerializer(author)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        user = self.request.user
        author = CustomUser.objects.get(id=user_id)
        try:
            follow = Follow.objects.get(user=user, author=author)
            follow.delete()
            return Response('Удалено',
                            status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response('Подписки не было',
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def showfollows(request):
    users = request.user.follower.all()
    user_obj = []
    for follow_obj in users:
        user_obj.append(follow_obj.author)
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(user_obj, request)
    serializer = UserFollowSerializer(
        result_page, many=True, context={'current_user': request.user}
    )
    return paginator.get_paginated_response(serializer.data)


class FavoriteViewSet(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                'Вы уже добавили рецепт в избранное',
                status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=user, recipe=recipe)
        serializer = AddFavouriteRecipeSerializer(recipe)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            add_favourite = Favorite.objects.get(user=user, recipe=recipe)
            add_favourite.delete()
            return Response('Удалено',
                            status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response('Рецепт не был в избранном',
                            status=status.HTTP_400_BAD_REQUEST)


class ShoppingVeiwSet(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, recipe_id):
        user = request.user
        purchase = get_object_or_404(Recipe, id=recipe_id)
        if ShoppingList.objects.filter(user=user, purchase=purchase).exists():
            return Response(
                'Вы уже добавили рецепт в список покупок',
                status=status.HTTP_400_BAD_REQUEST)
        ShoppingList.objects.create(user=user, purchase=purchase)
        serializer = AddFavouriteRecipeSerializer(purchase)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, recipe_id):
        user = request.user
        purchase = get_object_or_404(Recipe, id=recipe_id)
        try:
            add_to_shoppinglist = ShoppingList.objects.get(
                user=user,
                purchase=purchase
            )
            add_to_shoppinglist.delete()
            return Response('Удалено',
                            status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response('Рецепт не был в списке покупок',
                            status=status.HTTP_400_BAD_REQUEST)


class DownloadShoppingCart(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        users_shopping_list_recipes = user.user_shopping_lists.all()
        recipes = []
        for i in users_shopping_list_recipes:
            recipes.append(i.purchase)
        ingredients = []
        for recipe in recipes:
            ingredients.append(recipe.ingredients.all())
        new_ingredients = []
        for set in ingredients:
            for ingredient in set:
                new_ingredients.append(ingredient)
        ingredients_dict = {}
        for ing in new_ingredients:
            if ing in ingredients_dict.keys():
                ingredients_dict[ing] += ing.amount
            else:
                ingredients_dict[ing] = ing.amount
        wishlist = []
        for k, v in ingredients_dict.items():
            wishlist.append(f'{k.name} - {v} {k.measurement_unit} \n')
        wishlist.append('\n')
        wishlist.append('FoodGram, 2021')
        response = HttpResponse(wishlist, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="wishlist.txt"'
        return response
