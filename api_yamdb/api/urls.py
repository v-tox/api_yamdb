from django.urls import include, path
from rest_framework.routers import DefaultRouter
from api.views import (UserViewSet, NewUserView, TokenView,
                       CategoryViewSet, GenreViewSet, TitleViewSet,
                       ReviewViewSet, CommentViewSet
                       )

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(r'categories', CategoryViewSet, basename='categories'),
router_v1.register(r'genres', GenreViewSet, basename='genres'),
router_v1.register(r'titles', TitleViewSet, basename='titles'),
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', NewUserView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
]
