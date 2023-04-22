"""
In this file we configure url for authentication
"""

# third party import
from rest_framework import routers
from django.urls import path, include

# Local import
from authentication.views import LoginViewSet, RegisterViewSet, ProfileViewSet, RefreshTokenView, LogoutViewset

# creating objects or registering a router
router = routers.DefaultRouter()

router.register('register', RegisterViewSet, basename='login'),
router.register('login', LoginViewSet, basename='register'),
router.register('logout', LogoutViewset, basename='refresh'),
router.register('refresh', RefreshTokenView, basename='refresh'),
router.register('get-profile', ProfileViewSet, basename='profile')


urlpatterns = [
    path(r'', include(router.urls)),
]