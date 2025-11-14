from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django import forms
from .models import Listing, Category, Amenity, ListingImage, Location, PropertyType
from apps.agents.models import Agent


class SuperuserOnlyAdminMixin:
    """Mixin to restrict admin access to superusers only"""
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Location)
class LocationAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'created_at')
    list_filter = ('country', 'state', 'city', 'created_at')
    search_fields = ('name', 'city', 'state', 'country')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Location Information', {
            'fields': ('name', 'city', 'state', 'country')
        }),
        ('Coordinates', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(Amenity)
class AmenityAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(PropertyType)
class PropertyTypeAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(ListingImage)
class ListingImageAdmin(SuperuserOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('listing', 'is_main', 'created_at')
    list_filter = ('is_main', 'created_at')
    search_fields = ('listing__title', 'alt_text')
    readonly_fields = ('created_at',)


class AgentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Show the agent by their user's email (and agency name if available)
        try:
            return f"{obj.user.email} ({obj.agency_name})"
        except Exception:
            return str(obj)


class ListingAdminForm(forms.ModelForm):
    agent = AgentModelChoiceField(queryset=Agent.objects.all(), required=False)

    class Meta:
        model = Listing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make amenities optional in the admin form (it's already blank=True on the model)
        if 'amenities' in self.fields:
            self.fields['amenities'].required = False


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    form = ListingAdminForm
    # Remove `user` from admin forms entirely; we'll link user to agent.user on save
    exclude = ('user',)
    list_display = ('title', 'agent', 'location', 'price', 'status', 'is_published', 'is_featured', 'created_at')
    list_filter = ('status', 'is_published', 'is_featured', 'agent', 'property_type_obj', 'location')
    search_fields = ('title', 'description', 'agent_location')
    list_editable = ('status', 'is_published', 'is_featured')
    date_hierarchy = 'created_at'
    raw_id_fields = ('agent',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'price', 'status', 'is_published', 'is_featured', 'is_active')
        }),
        ('Property Details', {
            'fields': ('property_type_obj', 'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built', 'garage_spaces'),
            'classes': ('collapse',)
        }),
        ('Amenities & Category', {
            'fields': ('category', 'amenities'),
            'classes': ('collapse',)
        }),
        ('Location', {
            'fields': ('location', 'agent_location'),
            'description': 'Select from Location model or provide agent-provided details for later review'
        }),
        ('Assignment', {
            'fields': ('agent',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # If an agent is selected, associate the listing.user with the agent's user
        if obj.agent and hasattr(obj.agent, 'user'):
            obj.user = obj.agent.user
        else:
            # If no agent selected, leave user as-is (model allows null)
            obj.user = None
        super().save_model(request, obj, form, change)
