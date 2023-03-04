from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet,
                       GenreViewSet, TitleViewSet
                       )
# from django.urls import include, path
# from rest_framework.routers import DefaultRouter

# from api.views import (UserViewSet)

# app_name = 'api'

router = DefaultRouter()

# router.register(r'users', UserViewSet, basename='users')
router.register(r'^categories', CategoryViewSet, basename='categories'),
router.register(r'^genres', GenreViewSet, basename='genres'),
router.register(r'^titles', TitleViewSet, basename='titles'),
