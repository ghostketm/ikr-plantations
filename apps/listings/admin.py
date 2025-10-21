from django.contrib import admin
from .models import Category, Location, Amenity, Listing, ListingImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'latitude', 'longitude')
    list_filter = ('country', 'state')
    search_fields = ('name', 'city', 'state')


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 0


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'agent', 'category', 'location', 'property_type', 'status', 'price', 'is_featured', 'is_active', 'created_at')
    list_filter = ('property_type', 'status', 'is_featured', 'is_active', 'category', 'location', 'created_at')
    search_fields = ('title', 'description', 'agent__email')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ListingImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'property_type', 'status')
        }),
        ('Relationships', {
            'fields': ('agent', 'category', 'location', 'amenities')
        }),
        ('Pricing', {
            'fields': ('price', 'price_per_sqft')
        }),
        ('Property Details', {
            'fields': ('bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built', 'garage_spaces')
        }),
        ('Additional Information', {
            'fields': ('is_featured', 'is_active', 'views_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
