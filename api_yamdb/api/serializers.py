from datetime import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import validate_username


class UserCreateSerializer(serializers.Serializer):
    """Serializer of User create."""

    username = serializers.CharField(
        max_length=settings.LEN_USER_FIELDS,
        validators=[validate_username],
        required=True
    )
    email = serializers.EmailField(
        max_length=settings.LEN_EMAIL,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'email'
        )


class UserRecieveTokenSerializer(serializers.Serializer):
    """Serializer of User JWT token."""

    username = serializers.CharField(
        validators=[validate_username],
        max_length=settings.LEN_USER_FIELDS,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=settings.LEN_USER_FIELDS,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer of User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        validate_username(username)
        return username


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer of Review."""

    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('title',)

    def validate(self, data):
        """Ban on repeat reviews."""
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serializer of Comment."""

    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            'id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer of Category."""

    class Meta:
        model = Category
        fields = 'name', 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Serializer of Genre."""

    class Meta:
        model = Genre
        fields = 'name', 'slug'


class TitleGETSerializer(serializers.ModelSerializer):
    """Serializer of GET_Title."""
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )
        read_only_fields = ('__all__',)


class TitleSerializer(serializers.ModelSerializer):
    """Serializer of Title_notGET."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    year = serializers.IntegerField(
        validators=[
            MinValueValidator(
                0,
                message='Значение года не может быть отрицательным'
            ),
            MaxValueValidator(
                int(datetime.now().year),
                message='Значение года не может быть больше текущего'
            )
        ],
    )

    class Meta:
        model = Title
        fields = (
            'name', 'year', 'description', 'genre', 'category')

    def to_representation(self, title):
        """Choose serializer to read."""
        return TitleGETSerializer(title).data
