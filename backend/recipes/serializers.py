from rest_framework import serializers
from users.models import CustomUser
from users.serializers import UserSerializer

from .models import Follow, Ingredient, Recipe, ShoppingList, Tag


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    measurement_unit = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True, min_value=1)

    class Meta:
        fields = ('id', 'name', 'amount', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=True,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Recipe
        exclude = ('id', 'is_favorited', 'is_in_shopping_cart', 'author')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    tags = TagSerializer(
        many=True,
        read_only=True
    )
    ingredients = IngredientSerializer(
        many=True,
    )
    is_favorited = UserSerializer(many=True, read_only=True,)
    is_in_shopping_cart = UserSerializer(many=True, read_only=True,)

    class Meta:
        fields = ('__all__')
        model = Recipe


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('__all__')


class ShoppingListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    purchase = RecipeSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = ShoppingList


class AddFavouriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('name', 'image', 'cooking_time')


class ShowFollowersSerializer(serializers.ModelSerializer):
    recipes = RecipeCreateSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField('count_author_recipes')
    is_subscribed = serializers.SerializerMethodField('check_if_subscribed')

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def count_author_recipes(self, user):
        recipes_count = len(user.recipes.all())
        return recipes_count

    def check_if_subscribed(self, user):
        is_subscribed = len(user.following.all())
        if is_subscribed == 0:
            return False
        else:
            return True


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('name', 'image', 'cooking_time')


class UserFollowSerializer(serializers.ModelSerializer):
    recipes = RecipeCreateSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name',
                  'last_name', 'recipes',)
