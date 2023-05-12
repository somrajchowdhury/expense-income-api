"""API view classes for authentication application."""


from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer


class RegisterView(generics.GenericAPIView):
    """Add new users to database."""

    serializer_class = UserSerializer

    def post(self, request):
        """Create and save new user object."""
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serialized_user_data = serializer.data
        return Response(serialized_user_data, status=status.HTTP_201_CREATED)

