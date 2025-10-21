import django_filters
from .models import Listing, Category, Location
from .forms import ListingSearchForm


class ListingFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_query')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    location = django_filters.ModelChoiceFilter(queryset=Location.objects.all())
    property_type = django_filters.ChoiceFilter(choices=Listing.PROPERTY_TYPE)
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    bedrooms = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    bathrooms = django_filters.NumberFilter(field_name='bathrooms', lookup_expr='gte')

    class Meta:
        model = Listing
        fields = ['query', 'category', 'location', 'property_type', 'min_price', 'max_price', 'bedrooms', 'bathrooms']

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        ) | queryset.filter(
            description__icontains=value
        ) | queryset.filter(
            location__name__icontains=value
        ) | queryset.filter(
            category__name__icontains=value
        )
