from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime as dt
from users.models import User


PER_PAGE: int = 10


def current_year():
    return dt.datetime.today().year


class Title(models.Model):
    """Модель произведений"""
    category = models.ForeignKey(
        'Category',
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenre',
    )
    name = models.CharField(max_length=200)
    year = models.IntegerField(default=current_year,)
    description = models.TextField(max_length=200, null=True,)

    def __str__(self) -> str:
        return self.category[:PER_PAGE]


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(max_length=200,)
    slug = models.SlugField(
        max_length=50, unique=True,
    )

    def __str__(self) -> str:
        return self.slug[:PER_PAGE]


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=50, unique=True,)

    def __str__(self) -> str:
        return self.slug[:PER_PAGE]


class TitleGenre(models.Model):
    """Модель для ManyToMane Title"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    """Модель отзыва."""
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message="Оценка должна быть больше или равна 1"
            ),
            MaxValueValidator(
                10, message="Оценка должна быть меньше или равна 10"
            ),
        ],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    class Meta:
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            ),
        ]

    def __str__(self):
        return f'{self.title}, {self.score}, {self.author}'


class Comment(models.Model):
    """Модель комментария."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        max_length=200,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    def __str__(self):
        return self.text
