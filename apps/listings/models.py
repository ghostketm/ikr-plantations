from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='FontAwesome icon class')
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Location(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        ordering = ['country', 'state', 'city']
        unique_together = ['name', 'city', 'state']
    
    def __str__(self):
        return f'{self.name}, {self.city}, {self.state}'


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text='FontAwesome icon class')
    
    class Meta:
        verbose_name_plural = 'Amenities'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    PROPERTY_TYPE = (
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
    )
    
    STATUS = (
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('pending', 'Pending'),
    )
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE)
    status = models.CharField(max_length=20, choices=STATUS, default='available')
    
    # Relationships
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    amenities = models.ManyToManyField(Amenity, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Property Details
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    square_feet = models.PositiveIntegerField(help_text='Total area in square feet')
    lot_size = models.PositiveIntegerField(null=True, blank=True, help_text='Lot size in square feet')
    year_built = models.PositiveIntegerField(null=True, blank=True)
    garage_spaces = models.PositiveIntegerField(default=0)
    
    # Additional Information
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['property_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.square_feet and self.price:
            self.price_per_sqft = self.price / self.square_feet
        super().save(*args, **kwargs)
    
    def get_main_image(self):
        first_image = self.images.first()
        return first_image.image.url if first_image else None


class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
    
    def __str__(self):
        return f'Image for {self.listing.title}'
    
    def save(self, *args, **kwargs):
        if self.is_main:
            ListingImage.objects.filter(listing=self.listing, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
