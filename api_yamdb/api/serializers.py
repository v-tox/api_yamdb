from rest_framework import serializers

from reviews.models import (Category,
                            Genre,
                            Title,
                            current_year
                            )


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

    # Сюда метод подсчета рейтинга
