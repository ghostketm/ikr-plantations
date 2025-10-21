from django.db import models
from django.contrib.auth import get_user_model
from apps.listings.models import Listing

User = get_user_model()


class Inquiry(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='inquiries')
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f"Inquiry #{self.id} - {self.subject or 'General Inquiry'} from {self.user.email}"

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.email
