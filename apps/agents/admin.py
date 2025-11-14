from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Agent

User = get_user_model()


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency_name', 'license_number', 'verification_status', 'rating', 'is_featured', 'is_active')
    list_filter = ('verification_status', 'is_featured', 'is_active', 'created_at')
    search_fields = ('user__email', 'agency_name', 'license_number')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['deactivate_agents']

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Agency Information', {
            'fields': ('agency_name', 'license_number', 'years_of_experience', 'specialization', 'description')
        }),
        ('Contact Information', {
            'fields': ('office_address', 'website', 'facebook', 'twitter', 'linkedin', 'instagram')
        }),
        ('Verification and Rating', {
            'fields': ('verification_status', 'rating', 'total_listings', 'total_sales', 'is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def deactivate_agents(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} agent(s) have been deactivated.', messages.SUCCESS)
    deactivate_agents.short_description = "Deactivate selected agents"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.none()
        return qs

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
