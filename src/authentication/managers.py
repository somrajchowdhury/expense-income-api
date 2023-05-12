"""Custom model managers for authentication application."""

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Custom user model manager."""
    
    def create_user(self, username, email, password=None):
        """Create and save a user with specified fields."""
        if not username:
            raise ValueError("Username must be set!")
        if not email:
            raise ValueError("Email must be set!")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
        
    def create_superuser(self, username, email, password):
        """Create a save a superuser with specified fields."""
        if not password:
            raise ValueError("Password must be set!")
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

