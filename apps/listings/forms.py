from django import forms
from .models import Listing, Category, Location, Amenity, ListingImage


class ListingForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        help_text='Upload multiple images for the listing'
    )

    class Meta:
        model = Listing
        fields = [
            'title', 'description', 'property_type', 'category', 'price',
            'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built',
            'garage_spaces', 'location', 'amenities', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'location': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].queryset = Location.objects.all()
        self.fields['category'].queryset = Category.objects.all()


class ListingSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='All Categories'
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        empty_label='All Locations'
    )
    property_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Listing.PROPERTY_TYPE),
        required=False
    )
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    bedrooms = forms.IntegerField(required=False, min_value=0)
    bathrooms = forms.IntegerField(required=False, min_value=0)
