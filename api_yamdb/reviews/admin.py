from django.conf import settings
from django.contrib import admin
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category Admin."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Genre Admin."""

    list_display = (
        'pk',
        'name',
        'slug'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Title Admin."""

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        'get_genre',
        'count_reviews',
        'get_rating'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('name',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('name', 'year', 'category')

    def get_genre(self, object):
        """Get Genre or list_Genre."""
        return ', '.join(genre.name for genre in object.genre.all())

    get_genre.short_description = 'Жанр/ы произведения'

    def count_reviews(self, object):
        """Count Reviews."""
        return object.reviews.count()

    count_reviews.short_description = 'Количество отзывов'

    def get_rating(self, object):
        """Rating Title."""
        return (object.reviews.aggregate(
            average_score=Avg('score')).get('average_score'))

    get_rating.short_description = 'Рейтинг'


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    """GenreTitle Admin."""

    list_display = (
        'pk',
        'genre',
        'title'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('genre',)
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review Admin."""

    list_display = (
        'pk',
        'author',
        'text',
        'score',
        'pub_date',
        'title'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'score', 'pub_date')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment Admin."""

    list_display = (
        'pk',
        'author',
        'text',
        'pub_date',
        'review'
    )
    empty_value_display = 'значение отсутствует'
    list_filter = ('author', 'pub_date')
    list_per_page = settings.LIST_PER_PAGE
    search_fields = ('author',)


admin.site.site_title = 'Администрирование YaMDb'
admin.site.site_header = 'Администрирование YaMDb'
