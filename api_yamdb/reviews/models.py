from django.db import models
import datetime as dt
# from users.models import User для отзывов и комментов


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
        max_length=100, unique=True,
    )

    def __str__(self) -> str:
        return self.slug[:PER_PAGE]


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(max_length=200,)
    slug = models.SlugField(max_length=100, unique=True,)

    def __str__(self) -> str:
        return self.slug[:PER_PAGE]
