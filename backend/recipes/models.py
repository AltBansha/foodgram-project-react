from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Тег',
        unique=True
    )
    color = models.CharField(
        max_length=200,
        unique=True
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Укажите название ингредиента'
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
        help_text='Укажите единицу измерения'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=1,
        validators=[MinValueValidator(1), ]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Тег',
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='ingredients',
        verbose_name='Ингредиент',
    )
    is_favorited = models.ManyToManyField(
        CustomUser,
        default=None,
        related_name='is_favorited',
        verbose_name='Сохранившие'
    )
    is_in_shopping_cart = models.ManyToManyField(
        CustomUser,
        related_name='is_in_shopping_cart',
        verbose_name='В списке покупок'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200,
        help_text='Напишите название рецепта'
    )
    image = models.ImageField(
        upload_to='media/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Добавьте сюда описание рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1440)],
        verbose_name='Время приготовления в минутах',
        help_text='Укажите Время приготовления в минутах',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorites',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
    )

    class Meta:
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorites_recipes')
        ]

    def __str__(self):
        return f'Пользователь: {self.user}, \
                избранные рецепты: {self.recipe.name}'


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_follow')
            ]

    def __str__(self):
        return self.author.username


class ShoppingList(models.Model):
    user = models.ForeignKey(
        CustomUser,
        related_name='user_shopping_lists',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    purchase = models.ForeignKey(
        Recipe,
        related_name='purchase',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return f'Пользователь: {self.user.username}, покупает:{self.purchase}'
