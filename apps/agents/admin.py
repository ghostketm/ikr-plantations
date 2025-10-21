from django.contrib import admin
from .models import AgentProfile


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency_name', 'license_number', 'verification_status', 'rating', 'is_featured')
    list_filter = ('verification_status', 'is_featured', 'created_at')
    search_fields = ('user__email', 'agency_name', 'license_number')
    readonly_fields = ('created_at', 'updated_at')
    
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
            'fields': ('verification_status', 'rating', 'total_listings', 'total_sales', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
