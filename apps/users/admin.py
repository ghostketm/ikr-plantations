from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Profile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'city', 'country', 'created_at')
    list_filter = ('country', 'city', 'created_at')
    search_fields = ('user__email', 'user__username', 'phone_number', 'city')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'city', 'state', 'country', 'zip_code')
        }),
        ('Additional Information', {
            'fields': ('bio', 'avatar')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )