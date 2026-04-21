from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, SeekerProfile, OwnerProfile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role  = forms.ChoiceField(choices=User.Role.choices)
    city  = forms.CharField(max_length=100, required=False)

    class Meta:
        model  = User
        fields = ['username', 'email', 'role', 'city', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['username', 'email', 'phone', 'bio', 'city', 'avatar']

class SeekerProfileForm(forms.ModelForm):
    class Meta:
        model   = SeekerProfile
        exclude = ['user', 'created_at']
        widgets = {
            'move_in_date': forms.DateInput(attrs={'type': 'date'}),
            'budget_min'  : forms.NumberInput(attrs={'min': 0}),
            'budget_max'  : forms.NumberInput(attrs={'min': 0}),
        }

class OwnerProfileForm(forms.ModelForm):
    class Meta:
        model   = OwnerProfile
        exclude = ['user', 'created_at']