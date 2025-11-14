from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile
from apps.agents.models import Agent

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'city', 'state', 'country', 'zip_code', 'bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'city', 'state', 'country', 'zip_code', 'bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'bg-gray-700 text-white border-gray-600 rounded-md px-3 py-2 w-full'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'bg-gray-700 text-white border-gray-600 rounded-md px-3 py-2 w-full'}),
            'phone_number': forms.TextInput(attrs={'class': 'bg-gray-700 text-white border-gray-600 rounded-md px-3 py-2 w-full'}),
            'city': forms.TextInput(attrs={'class': 'bg-gray-700 text-white border-gray-600 rounded-md px-3 py-2 w-full'}),
            'state': forms.TextInput(attrs={'class': 'bg-gray-700 text-white border-gray-600 rounded-md px-3 py-2 w-full'}),
            'country': forms.TextInput(attrs={'class': 'bg-gray-700 text-white border-gray-600 rounded-md px-3 py-2 w-full'}),
            'zip_code': forms.TextInput(attrs={'class': 'bg-gray-700 text-white border-gray-600 rounded-md px-3 py-2 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        profile = super().save(commit=commit)
        return profile


