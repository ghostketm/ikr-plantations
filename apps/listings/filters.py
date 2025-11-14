import django_filters
from .models import Listing, Category
# from .forms import ListingSearchForm


class ListingFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_query')
    # category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    # location = django_filters.ModelChoiceFilter(queryset=Location.objects.all())
    # property_type = django_filters.ChoiceFilter(choices=Listing.PROPERTY_TYPE)
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte', method='filter_price')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte', method='filter_price')

    class Meta:
        model = Listing
        fields = ['query', 'min_price', 'max_price']

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        ) | queryset.filter(
            description__icontains=value
        )

    def filter_price(self, queryset, name, value):
        # This method is used for both min_price and max_price.
        # 'name' will be 'price__gte' or 'price__lte' based on lookup_expr.
        # We only filter if a value is provided.
        return queryset.filter(**{name: value}) if value is not None else queryset
