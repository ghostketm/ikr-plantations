from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }
