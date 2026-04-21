from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import RegisterForm, UserUpdateForm, SeekerProfileForm, OwnerProfileForm
from .models import SeekerProfile, OwnerProfile

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.role == 'seeker':
                SeekerProfile.objects.create(user=user)
            else:
                OwnerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to RoomieMatch!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, request.FILES, instance=user)

        if user.is_seeker():
            profile_form = SeekerProfileForm(request.POST, instance=user.seeker_profile)
        else:
            profile_form = OwnerProfileForm(request.POST, instance=user.owner_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)
        if user.is_seeker():
            profile_form = SeekerProfileForm(instance=user.seeker_profile)
        else:
            profile_form = OwnerProfileForm(instance=user.owner_profile)

    return render(request, 'accounts/profile.html', {
        'user_form'   : user_form,
        'profile_form': profile_form,
    })

def logout_view(request):
    logout(request)
    return redirect('home')