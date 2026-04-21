from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SeekerProfile, OwnerProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'role', 'city', 'is_active']
    list_filter   = ['role', 'is_active']
    search_fields = ['username', 'email']
    fieldsets     = UserAdmin.fieldsets + (
        ('RoomieMatch', {'fields': ('role', 'avatar', 'phone', 'bio', 'city')}),
    )

@admin.register(SeekerProfile)
class SeekerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'budget_min', 'budget_max', 'schedule', 'is_smoker', 'has_pets']

@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'accepts_pets', 'accepts_smoker', 'preferred_schedule']