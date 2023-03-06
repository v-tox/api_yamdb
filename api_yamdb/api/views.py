from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Genre, Title, Review, Comment
from api.permissions import (IsAdminOrReadOnly,
                             IsAuthorOrReadOnly)

from api.filters import TitleFilter
from api.serializers import (UserSerializer,
                             CategorySerializer,
                             GenreSerializer,
                             TitleViewSerializer,
                             TitleWriteSerializer,
                             ReviewSerializer,
                             CommentSerializer)

# class UserViewSet(viewsets.ModelViewSet):


class MixinViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""
    queryset = Title.objects.all().annotate(Avg('reviews__score'))
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleViewSerializer


class GenreViewSet(MixinViewSet):
    """Вьюсет жанров."""
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(MixinViewSet):
    """Вьюсет категорий."""
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя."""
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецензий."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.select_related('author').all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_rewiew(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_title().review.comments.select_related('author').all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_rewiew())
