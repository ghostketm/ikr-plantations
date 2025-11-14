
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Agent(models.Model):
    VERIFICATION_STATUS = (
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    agency_name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    office_address = models.TextField(blank=True)
    website = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS, 
        default='pending'
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_listings = models.PositiveIntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.user.email} - {self.agency_name}'
    
    def get_contact_email(self):
        return self.user.email

    def get_full_name(self):
        return self.user.get_full_name()

    def get_contact_phone(self):
        return self.user.profile.phone_number if hasattr(self.user, 'profile') else ''

class Rating(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('agent', 'user')
