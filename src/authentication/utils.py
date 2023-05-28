"""Utility class definitions for authentication application."""


from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from .models import User


class EmailUtil:
    """Utility class to handle sending of emails."""

    @staticmethod
    def send_verification_email(data):
        """Send email to recipient."""
        # Create custom email subject and HTML body
        subject = "Verify your email"
        body = """
        <div style="font-family: Helvetica, sans-serif;">
            <h3>Hi {}!</h3>
            Use link below to verify your email:<br/><br/>
            <a style="text-decoration: none;" href="{}">{}</a>
        </div>
        """.format(data["user"].username, data["url"], data["url"])
        # send email
        email = EmailMessage(subject=subject,
                             body=body,
                             to=[data["user"].email,])
        email.content_subtype = "html"
        email.send()


class TokenUtil:
    """Utility class to handle generation of access & refresh tokens."""

    @staticmethod
    def generate_access_token(user):
        """Generate access token for user."""
        access_token = RefreshToken.for_user(user).access_token
        return access_token


class UserUtil:
    """Utility class to get user objects by username or email."""

    @staticmethod
    def get_user_by_email(email):
        """Search user by email."""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


class URLUtil:
    """Utility class for constructing formatted urls."""

    @staticmethod
    def get_email_verification_url(domain, view_urlpattern, token):
        """Construct email verification url."""
        url = "http://{}{}?token={}".format(domain, view_urlpattern, token)
        return url

