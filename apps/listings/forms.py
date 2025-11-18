from django import forms
from .models import Listing, Amenity, ListingImage, Location, Category
from .models import PropertyType

class ListingForm(forms.ModelForm):
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    images = forms.FileField(
        required=False,
        help_text='Upload images for the listing (you can select multiple files)'
    )
    # Hidden field to track which images to delete
    images_to_delete = forms.CharField(
        widget=forms.HiddenInput(), required=False
    )
    property_type_obj = forms.ModelChoiceField(
        queryset=PropertyType.objects.all(),
        required=False,
        empty_label='Select a Property Type',
        label='Property Type'
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        empty_label="Select a Location",
        required=True
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a Category",
        required=True
    )

    class Meta:
        model = Listing
        fields = [
            'title', 'property_type_obj', 'category', 'status', 'description', 'price',
            'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built', 'garage_spaces',
            'location', 'amenities', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
