from django import forms
from .models import Listing, ListingPhoto

class ListingForm(forms.ModelForm):
    class Meta:
        model   = Listing
        exclude = ['owner', 'status', 'created_at', 'updated_at']
        widgets = {
            'available_from': forms.DateInput(attrs={'type': 'date'}),
            'description'   : forms.Textarea(attrs={'rows': 5}),
            'price'         : forms.NumberInput(attrs={'min': 0}),
            'size'          : forms.NumberInput(attrs={'min': 1}),
        }

class ListingPhotoForm(forms.ModelForm):
    class Meta:
        model  = ListingPhoto
        fields = ['image', 'caption']

# Multiple photos upload
ListingPhotoFormSet = forms.inlineformset_factory(
    Listing,
    ListingPhoto,
    form   = ListingPhotoForm,
    extra  = 3,    # 3 empty slots by default
    max_num = 10,  # max 10 photos
    can_delete = True
)

class ListingFilterForm(forms.Form):
    """Filter form for listing list page"""
    city      = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'City...'}))
    price_min = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Min price'}))
    price_max = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={'placeholder': 'Max price'}))
    room_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All types')] + list(Listing.RoomType.choices)
    )
    pets_allowed    = forms.BooleanField(required=False)
    smoking_allowed = forms.BooleanField(required=False)