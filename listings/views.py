from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Listing
from .forms import ListingForm, ListingPhotoFormSet, ListingFilterForm
from visits.tasks import send_listing_created_email
from matching.utils import calculate_score 

def listing_list(request):
    listings = Listing.objects.filter(status='active').prefetch_related('photos')
    form     = ListingFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('city'):
            listings = listings.filter(city__icontains=form.cleaned_data['city'])
        if form.cleaned_data.get('price_min'):
            listings = listings.filter(price__gte=form.cleaned_data['price_min'])
        if form.cleaned_data.get('price_max'):
            listings = listings.filter(price__lte=form.cleaned_data['price_max'])
        if form.cleaned_data.get('room_type'):
            listings = listings.filter(room_type=form.cleaned_data['room_type'])
        if form.cleaned_data.get('pets_allowed'):
            listings = listings.filter(pets_allowed=True)
        if form.cleaned_data.get('smoking_allowed'):
            listings = listings.filter(smoking_allowed=True)

    paginator   = Paginator(listings, 9)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)

    #  Si requête HTMX → retourne seulement la grille
    if request.htmx:
        return render(request, 'listings/partials/listings_grid.html', {
            'page_obj': page_obj,
        })

    return render(request, 'listings/list.html', {
        'page_obj': page_obj,
        'form'    : form,
    })

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk, status='active')
    score   = None

    if request.user.is_authenticated and request.user.is_seeker():
        try:
            score = calculate_score(request.user.seeker_profile, listing)
        except Exception:
            pass

    return render(request, 'listings/detail.html', {
        'listing': listing,
        'score'  : score,
    })

@login_required
def listing_create(request):
    if not request.user.is_owner():
        messages.error(request, 'Only owners can post listings.')
        return redirect('dashboard')

    if request.method == 'POST':
        form     = ListingForm(request.POST)
        formset  = ListingPhotoFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            listing       = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            formset.instance = listing
            formset.save()
            send_listing_created_email.delay(listing.id)
            messages.success(request, 'Listing posted successfully!')
            return redirect('listings:detail', pk=listing.pk)
    else:
        form    = ListingForm()
        formset = ListingPhotoFormSet()

    return render(request, 'listings/create.html', {
        'form'   : form,
        'formset': formset,
    })

@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)

    if request.method == 'POST':
        form    = ListingForm(request.POST, instance=listing)
        formset = ListingPhotoFormSet(request.POST, request.FILES, instance=listing)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Listing updated!')
            return redirect('listings:detail', pk=listing.pk)
    else:
        form    = ListingForm(instance=listing)
        formset = ListingPhotoFormSet(instance=listing)

    return render(request, 'listings/edit.html', {
        'form'   : form,
        'formset': formset,
        'listing': listing,
    })

@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing deleted.')
        return redirect('listings:my_listings')
    return render(request, 'listings/confirm_delete.html', {'listing': listing})

@login_required
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user).prefetch_related('photos')
    return render(request, 'listings/my_listings.html', {'listings': listings})