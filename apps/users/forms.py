from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Profile
from apps.agents.models import AgentProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'city', 'state', 'country', 'zip_code', 'bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)

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
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['email'].initial = self.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name')
            self.user.last_name = self.cleaned_data.get('last_name')
            self.user.email = self.cleaned_data.get('email')
            if commit:
                self.user.save()
        if commit:
            profile.save()
        return profile

class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = ('agency_name', 'license_number', 'years_of_experience', 'specialization', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'specialization': forms.Textarea(attrs={'rows': 3}),
        }
