from django.contrib import admin
from .models import CompatibilityScore

@admin.register(CompatibilityScore)
class CompatibilityScoreAdmin(admin.ModelAdmin):
    list_display  = ['seeker', 'listing', 'score', 'computed_at']
    list_filter   = ['score']
    ordering      = ['-score']