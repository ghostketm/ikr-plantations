import django_filters
from .models import Agent


class AgentFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_query')
    agency_name = django_filters.CharFilter(field_name='agency_name', lookup_expr='icontains')
    specialization = django_filters.CharFilter(field_name='specialization', lookup_expr='icontains')
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    min_experience = django_filters.NumberFilter(field_name='years_of_experience', lookup_expr='gte')
    max_experience = django_filters.NumberFilter(field_name='years_of_experience', lookup_expr='lte')

    class Meta:
        model = Agent
        fields = ['query', 'agency_name', 'specialization', 'min_rating', 'max_rating', 'min_experience', 'max_experience']

    def filter_query(self, queryset, name, value):
        return queryset.filter(
            user__username__icontains=value
        ) | queryset.filter(
            agency_name__icontains=value
        ) | queryset.filter(
            specialization__icontains=value
        )
