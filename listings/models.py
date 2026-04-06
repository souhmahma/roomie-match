from django.db import models
from accounts.models import User

class Listing(models.Model):
    class Status(models.TextChoices):
        ACTIVE   = 'active',   'Active'
        INACTIVE = 'inactive', 'Inactive'
        RENTED   = 'rented',   'Rented'

    class RoomType(models.TextChoices):
        PRIVATE = 'private', 'Private room'
        SHARED  = 'shared',  'Shared room'
        STUDIO  = 'studio',  'Studio'

    owner       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title       = models.CharField(max_length=200)
    description = models.TextField()
    city        = models.CharField(max_length=100)
    address     = models.CharField(max_length=255, blank=True)
    price       = models.PositiveIntegerField(help_text='Monthly rent in €')
    size        = models.PositiveIntegerField(help_text='Room size in m²')
    room_type   = models.CharField(max_length=20, choices=RoomType.choices, default=RoomType.PRIVATE)
    status      = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    # House rules
    pets_allowed   = models.BooleanField(default=False)
    smoking_allowed = models.BooleanField(default=False)
    students_allowed = models.BooleanField(default=True)

    # Preferred lifestyle
    preferred_schedule = models.CharField(
        max_length=20,
        choices=[('early', 'Early bird'), ('night', 'Night owl'), ('normal', 'Standard')],
        default='normal'
    )
    preferred_noise = models.CharField(
        max_length=20,
        choices=[('quiet', 'Quiet'), ('medium', 'Moderate'), ('loud', 'Lively')],
        default='medium'
    )

    available_from = models.DateField()
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {self.city} ({self.price}€/month)"

    def get_main_photo(self):
        return self.photos.first()


class ListingPhoto(models.Model):
    listing  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='photos')
    image    = models.ImageField(upload_to='listings/')
    caption  = models.CharField(max_length=100, blank=True)
    order    = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Photo #{self.order} — {self.listing.title}"