from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email', 'listing__title', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Inquiry Information', {
            'fields': ('user', 'listing', 'subject', 'message', 'email', 'phone')
        }),
        ('Status', {
            'fields': ('status', 'responded_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
