from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewsSet, TitleViewSet, UserCreateViewSet,
                       UserReceiveTokenViewSet, UserViewSet)
from django.urls import include, path
from rest_framework import routers

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewsSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

auth_urls = [
    path(
        'signup/', UserCreateViewSet.as_view(),
        name='signup'),
    path(
        'token/', UserReceiveTokenViewSet.as_view(),
        name='token')
]

urlpatterns = [
    path('v1/auth/', include(auth_urls)),
    path('v1/', include(router_v1.urls))
]
