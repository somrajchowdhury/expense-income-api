"""API view classes for authentication application."""


from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .serializers import UserSerializer
from .utils import EmailUtil, TokenUtil, UserUtil, URLUtil
import jwt
from .models import User
from django.conf import settings


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
        # get access token for user
        user = UserUtil.get_user_by_email(serialized_user_data["email"])
        token = TokenUtil.generate_access_token(user)
        # construct verification url
        domain = get_current_site(request).domain
        verification_url = \
            URLUtil.get_email_verification_url(domain, reverse("verify-email"),
                                               token)
        # send email verification email
        data = {"user": user, "url": verification_url}
        EmailUtil.send_verification_email(data)
        return Response(serialized_user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    """Verify user email."""

    def get(self, request):
        """Decode token and verify user email."""
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token,
                                 settings.SECRET_KEY,
                                 algorithms=['HS256'])
            user = User.objects.get(id=payload["user_id"])
            # avoid unnecessary database update operations
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({"success": "Email verification successful."},
                            status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Activation link expired."},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token."},
                            status=status.HTTP_400_BAD_REQUEST)

