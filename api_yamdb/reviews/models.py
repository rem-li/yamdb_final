from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from reviews.validators import slug_validator, year_validator
from users.models import User


class AbstractGenreCategories(models.Model):
    name = models.CharField(
        max_length=settings.LEN_NAME,
        verbose_name='Hазвание поля',
        db_index=True
    )
    slug = models.SlugField(
        max_length=settings.LEN_SLUG,
        verbose_name='slug',
        unique=True,
        validators=[slug_validator]
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.LEN_TEXT]


class Category(AbstractGenreCategories):
    """Class Category."""

    class Meta(AbstractGenreCategories.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(AbstractGenreCategories):
    """Class Genre."""

    class Meta(AbstractGenreCategories.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Class title."""

    name = models.CharField(
        max_length=settings.LEN_NAME,
        verbose_name='Hазвание',
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='год выпуска',
        validators=[year_validator],
        db_index=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', 'name')

    def __str__(self):
        return self.name[:settings.LEN_TEXT]


class GenreTitle(models.Model):
    """Class Genre_Title."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Таблица соответствия жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'


class AbstractCommentReview(models.Model):
    """Abstract Class for Review and Comment."""

    text = models.TextField(
        verbose_name='текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s',
        verbose_name='Aвтор'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        abstract = True
        default_related_name = 'reviews',

        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:settings.LEN_TEXT]


class Review(AbstractCommentReview):
    """Class Review."""

    score = models.PositiveSmallIntegerField(
        verbose_name='Oценка',
        default=1,
        validators=[
            MinValueValidator(
                1,
                message='Введенная оценка ниже допустимой'
            ),
            MaxValueValidator(
                10,
                message='Введенная оценка выше допустимой'
            ),
        ]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение',
        null=True
    )

    class Meta(AbstractCommentReview.Meta):
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = (
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            ),
        )


class Comment(AbstractCommentReview):
    """Class Comment"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='oтзыв',
    )

    class Meta(AbstractCommentReview.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
