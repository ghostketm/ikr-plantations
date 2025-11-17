from django import forms
from django.contrib.auth import get_user_model, authenticate
from allauth.account.forms import LoginForm
from .models import Profile

User = get_user_model()

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'bio', 'address', 'city', 'state', 'country', 'zip_code', 'avatar']


class CustomLoginForm(LoginForm):
    """
    Custom login form to provide specific error messages for email and password.
    """
    def clean(self):
        # The parent clean method is called, but it doesn't do validation.
        # We will perform our own validation here.
        cleaned_data = super().clean()

        email = self.cleaned_data.get('login')
        password = self.cleaned_data.get('password')

        if not email or not password:
            # If fields are empty, let the default validators handle it.
            return cleaned_data

        # Check if a user with the given email exists.
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            # Raise an error on the 'login' (email) field.
            raise forms.ValidationError({
                'login': "No account found with this email address. Please check your email or sign up."
            })

        # Authenticate the user.
        user = authenticate(request=self.request, username=email, password=password)
        if user is None:
            # If authentication fails, it means the password was incorrect.
            raise forms.ValidationError({
                'password': "The password you entered is incorrect. Please try again."
            })

        return cleaned_data