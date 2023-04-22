"""
In this class we create a model for authentication
"""

# Third Party imports
import  uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Local import
from .manager import CustomUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    create a table for user
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=128, blank=True)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def full_name(self):
        full_name = None
        if self.first_name and self.last_name:
            full_name = self.first_name + self.last_name
        if self.first_name:
            full_name = self.first_name
        return full_name

    class Meta:
        """class meta for user"""
        db_table = 'auth_user'
