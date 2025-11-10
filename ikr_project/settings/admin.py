from django.contrib import admin
from .models import AgentProfile


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for AgentProfile model.
    """
    list_display = ('user', 'phone_number', 'license_number', 'is_verified')
    search_fields = ('user__username', 'user__email', 'phone_number', 'license_number')
    list_filter = ('is_verified',)