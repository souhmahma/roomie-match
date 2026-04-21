from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SEEKER = 'seeker', 'Seeker'    # looking for a room
        OWNER  = 'owner',  'Owner'     # offering a room

    role   = models.CharField(max_length=20, choices=Role.choices, default=Role.SEEKER)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone  = models.CharField(max_length=20, blank=True)
    bio    = models.TextField(blank=True)
    city   = models.CharField(max_length=100, blank=True)

    def is_seeker(self):
        return self.role == self.Role.SEEKER

    def is_owner(self):
        return self.role == self.Role.OWNER

    def __str__(self):
        return f"{self.username} ({self.role})"


class SeekerProfile(models.Model):
    """Detailed seeker profile — used for matching"""

    class Schedule(models.TextChoices):
        EARLY  = 'early',  'Early bird'
        NIGHT  = 'night',  'Night owl'
        NORMAL = 'normal', 'Standard'

    class NoiseLevel(models.TextChoices):
        QUIET  = 'quiet',  'Quiet'
        MEDIUM = 'medium', 'Moderate'
        LOUD   = 'loud',   'Lively'

    user         = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seeker_profile')
    budget_min   = models.PositiveIntegerField(default=0)
    budget_max   = models.PositiveIntegerField(default=1000)
    schedule     = models.CharField(max_length=20, choices=Schedule.choices, default=Schedule.NORMAL)
    noise_level  = models.CharField(max_length=20, choices=NoiseLevel.choices, default=NoiseLevel.MEDIUM)
    has_pets     = models.BooleanField(default=False)
    is_smoker    = models.BooleanField(default=False)
    is_student   = models.BooleanField(default=False)
    move_in_date = models.DateField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


class OwnerProfile(models.Model):
    """Detailed owner profile"""
    user               = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile')
    accepts_pets       = models.BooleanField(default=False)
    accepts_smoker     = models.BooleanField(default=False)
    preferred_schedule = models.CharField(max_length=20, choices=SeekerProfile.Schedule.choices, default='normal')
    preferred_noise    = models.CharField(max_length=20, choices=SeekerProfile.NoiseLevel.choices, default='medium')
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Owner profile of {self.user.username}"