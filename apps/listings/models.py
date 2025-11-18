from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from apps.agents.models import Agent # Assuming Agent model is in apps.agents
from cloudinary.models import CloudinaryField

User = get_user_model()

class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Property Type'
        verbose_name_plural = 'Property Types'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['country', 'state', 'city']
        unique_together = ('name', 'city', 'state')
    
    def __str__(self):
        return f'{self.name}, {self.city}, {self.state}'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Amenities'

class ListingImage(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='listings', resource_type='image')
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"

    def get_image_url(self):
        """
        Return the image URL.
        - If the image file exists, it returns the full URL (local or Cloudinary).
        - If the image file is missing, it returns an empty string.
        This prevents broken image links and allows templates to handle fallbacks.
        """
        if self.image and hasattr(self.image, 'url'):
            try:
                return self.image.url
            except (ValueError, FileNotFoundError):
                pass  # The file is missing on storage
        return ""

class Listing(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    )

    PROPERTY_TYPE_CHOICES = (
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('condo', 'Condo'),
        ('townhouse', 'Townhouse'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings', null=True)
    agent = models.ForeignKey(Agent, on_delete=models.SET_NULL, null=True, blank=True, related_name='agent_listings')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings')
    property_type_obj = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings', verbose_name='Property Type')

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text='Price of the property')
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES, default='house', blank=True, help_text='Deprecated: use Property Type model instead')
    bedrooms = models.IntegerField(null=True, blank=True, help_text='Number of bedrooms (if applicable)')
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, help_text='Number of bathrooms (if applicable)')
    square_feet = models.IntegerField(null=True, blank=True, help_text='Total area in square feet')
    lot_size = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, help_text='Lot/land size in acres')
    year_built = models.IntegerField(null=True, blank=True, help_text='Year property was built (if applicable)')
    garage_spaces = models.IntegerField(null=True, blank=True, help_text='Number of garage spaces (if applicable)')
    agent_location = models.CharField(max_length=500, blank=True, default='', help_text='Agent-provided location details for later review')
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='listings')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Listing.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.price is None:
            self.price = Decimal('0.00')
        if not isinstance(self.price, (Decimal, int, float)) or self.price < 0:
            raise ValidationError({'price': 'Price must be a valid positive number.'})
