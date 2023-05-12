"""Model definitions for authentication application."""


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model."""

    username = models.CharField(max_length=255,
                                unique=True,
                                db_index=True)
    email = models.EmailField(max_length=255,
                              unique=True,
                              db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    objects = UserManager()

    def __str__(self):
        """Custom user object representation."""
        return self.email

