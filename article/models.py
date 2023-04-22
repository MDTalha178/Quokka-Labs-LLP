"""
In this class we create a model for Article
"""

import uuid
from django.db import models


# Create your models here.
from authentication.models import User


class Article(models.Model):
    """
    create a table for article into database
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_create_by')
    status = models.BooleanField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """class meta for user"""
        db_table = 'article'

