from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    """Custom adapter to handle email-based authentication for custom User model."""

    def pre_authenticate(self, request, **kwargs):
        """Pre-authenticate hook to handle email-based login."""
        email = kwargs.get('email') or kwargs.get('login')
        if email:
            kwargs['email'] = email.lower()
        return kwargs

    def populate_user(self, request, sociallogin, data):
        """Populate user data from social login."""
        user = super().populate_user(request, sociallogin, data)
        # Ensure username field is populated (can be same as email for our custom user)
        if not user.username:
            user.username = user.email
        return user

    def save_user(self, request, sociallogin, form=None):
        """Save user and handle email address record creation."""
        user = super().save_user(request, sociallogin, form)
        # Ensure EmailAddress record exists and is verified
        try:
            email_address, created = EmailAddress.objects.get_or_create(
                user=user,
                email=user.email.lower(),
                defaults={'verified': True, 'primary': True}
            )
            if not email_address.verified:
                email_address.verified = True
                email_address.save()
            if not email_address.primary:
                email_address.primary = True
                email_address.save()
        except IntegrityError:
            # Handle race condition where EmailAddress was created by another process
            pass
        return user
