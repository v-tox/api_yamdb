from django.shortcuts import get_object_or_404
from django.forms import ValidationError
from rest_framework import serializers

from users.models import User
from reviews.models import (Category,
                            Genre,
                            Title,
                            current_year,
                            Review,
                            Comment
                            )


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class NewUserSerializer(serializers.Serializer):
    """Сериалайзер нового пользоватея"""
    class Meta:
        model = User
        fields = (
            'username',
            'email'
        )


class TokenSerializer(serializers.Serializer):
    """Сериалайзер JWT-токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категорий."""
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанров."""
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False,
    )

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        many=False,
        required=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, year):
        """Валидация поля year."""
        if not (1800 < year <= current_year()):
            raise serializers.ValidationError('Год не подходит')
        return year


class TitleViewSerializer(serializers.ModelSerializer):
    """Сериалайзер произведений."""
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer(required=True,)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериалайзер рецензий"""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user).exists():
                raise ValidationError(
                    'Допустимо не более 1 отзыва на произведение')
        return data

    def validate_score(self, score):
        if score < 1 or score > 10:
            raise serializers.ValidationError(
                'Рейтинг произведения должен быть от 1 до 10')
        return score

    class Meta:
        fields = (
            'id', 'text', 'author', 'score', 'pub_date'
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Серилизатор комментариев"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.ReadOnlyField(
        source='review.id'
    )

    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date'
        )
        model = Comment
