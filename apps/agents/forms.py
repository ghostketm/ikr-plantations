
from django import forms
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from .models import Agent

User = get_user_model()

class AgentCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Select an existing user or leave blank to create new",
        required=False,
        help_text="Select an existing user to make them an agent, or leave blank to create a new user."
    )
    email = forms.EmailField(required=False, help_text="Required if creating a new user")
    username = forms.CharField(max_length=150, required=False, help_text="Required if creating a new user")

    class Meta:
        model = Agent
        fields = ('user', 'agency_name', 'license_number', 'years_of_experience', 'specialization', 'description', 'office_address', 'website', 'facebook', 'twitter', 'linkedin', 'instagram', 'verification_status')

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        email = cleaned_data.get('email')
        username = cleaned_data.get('username')

        if not user:
            if not email or not username:
                raise forms.ValidationError("Email and username are required when creating a new user.")
            # Check if user with this email or username already exists
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email already exists.")
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("A user with this username already exists.")
        else:
            # Check if user is already an agent
            if hasattr(user, 'agent'):
                raise forms.ValidationError("This user is already an agent.")

        return cleaned_data

    def save(self, commit=True):
        user = self.cleaned_data.get('user')
        if not user:
            # Generate a temporary password
            password = get_random_string(10)
            # Create new user
            user = User.objects.create_user(
                email=self.cleaned_data['email'],
                username=self.cleaned_data['username'],
                password=password
            )
            self.temp_password = password  # Store password to access in the view
        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance
