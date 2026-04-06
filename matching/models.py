from django.db import models
from accounts.models import User
from listings.models import Listing

class CompatibilityScore(models.Model):
    """Cache computed scores to avoid recalculating every time"""
    seeker    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    listing   = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='scores')
    score     = models.PositiveIntegerField()
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['seeker', 'listing']  # one score per pair
        ordering        = ['-score']

    def __str__(self):
        return f"{self.seeker.username} ↔ {self.listing.title} = {self.score}%"