from django.db import models
from accounts.models import User
from listings.models import Listing

class VisitRequest(models.Model):
    class Status(models.TextChoices):
        PENDING  = 'pending',  'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'
        CANCELLED = 'cancelled', 'Cancelled'

    seeker     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visit_requests')
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='visit_requests')
    status     = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    date       = models.DateField()
    time       = models.TimeField()
    message    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.seeker.username} → {self.listing.title} ({self.date})"


class Availability(models.Model):
    """Owner sets available days for visits"""
    owner      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='availabilities')
    date       = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['listing', 'date']
        ordering        = ['date']

    def __str__(self):
        return f"{self.listing.title} — {self.date} ({'available' if self.is_available else 'unavailable'})"

