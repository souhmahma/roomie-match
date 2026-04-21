from django import forms
from .models import VisitRequest, Availability
from django.utils import timezone

class VisitRequestForm(forms.ModelForm):
    class Meta:
        model   = VisitRequest
        fields  = ['date', 'time', 'message']
        widgets = {
            'date'   : forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'time'   : forms.TimeInput(attrs={'type': 'time'}),
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Introduce yourself...'}),
        }

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model   = Availability
        fields  = ['date', 'is_available']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }