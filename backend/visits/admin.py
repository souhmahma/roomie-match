from django.contrib import admin
from .models import VisitRequest, Availability

@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display  = ['seeker', 'listing', 'date', 'time', 'status', 'created_at']
    list_filter   = ['status']
    list_editable = ['status']
    search_fields = ['seeker__username', 'listing__title']

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['listing', 'date', 'is_available']
    list_filter  = ['is_available']