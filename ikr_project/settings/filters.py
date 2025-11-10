import django_filters
from django.db.models import Q
from .models import AgentProfile


class AgentFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_query', label="Search")

    class Meta:
        model = AgentProfile
        fields = ['query']

    def filter_by_query(self, queryset, name, value):
        return queryset.filter(
            Q(user__first_name__icontains=value) |
            Q(user__last_name__icontains=value) |
            Q(agency_name__icontains=value) |
            Q(specialization__icontains=value)
        )