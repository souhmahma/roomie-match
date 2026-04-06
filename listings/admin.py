from django.contrib import admin
from .models import Listing, ListingPhoto

class ListingPhotoInline(admin.TabularInline):
    model = ListingPhoto
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'city', 'price', 'status', 'created_at']
    list_filter   = ['status', 'room_type', 'pets_allowed', 'smoking_allowed']
    search_fields = ['title', 'city', 'owner__username']
    list_editable = ['status']
    inlines       = [ListingPhotoInline]