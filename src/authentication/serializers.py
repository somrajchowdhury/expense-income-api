"""Serializer classes for authentication application."""


from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer class for User model."""

    password = serializers.CharField(max_length=68,
                                     min_length=6,
                                     write_only=True)

    class Meta:
        """Meta class for UserSerializer."""

        model = User
        fields = ["email", "username", "password"]

    def validate(self, data):
        """Validate user entered data."""
        email = data.get('email', '')
        username = data.get('username', '')
        # username should only contain alphabets and numbers
        if not username.isalnum():
            raise serializers.ValidationError({
                "username": "The username must only contain alphanumeric"
                " characters."
            })
        return data

    def create(self, validated_data):
        """Create user object with validated data."""
        user = User.objects.create_user(**validated_data)
        return user

