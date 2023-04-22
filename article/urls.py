"""
In this file we configure url for article
"""

# third party import
from rest_framework import routers
from django.urls import path, include

# creating objects or registering a router
from article.views import ArticleViewSet

router = routers.DefaultRouter()

router.register('article', ArticleViewSet, basename='login')

urlpatterns = [
    path(r'', include(router.urls)),
]
