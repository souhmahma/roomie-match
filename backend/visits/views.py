from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VisitRequest, Availability
from .forms import VisitRequestForm, AvailabilityForm
from listings.models import Listing
from visits.tasks import (
    send_visit_request_email,
    send_visit_accepted_email,
    send_visit_declined_email
)

@login_required
def request_visit(request, listing_pk):
    """Seeker requests a visit"""
    listing = get_object_or_404(Listing, pk=listing_pk, status='active')

    if not request.user.is_seeker():
        messages.error(request, 'Only seekers can request visits.')
        return redirect('listings:detail', pk=listing_pk)

    # Check if already requested
    existing = VisitRequest.objects.filter(
        seeker  = request.user,
        listing = listing,
        status  = 'pending'
    ).first()

    if existing:
        messages.warning(request, 'You already have a pending visit request for this listing.')
        return redirect('listings:detail', pk=listing_pk)

    if request.method == 'POST':
        form = VisitRequestForm(request.POST)
        if form.is_valid():
            visit         = form.save(commit=False)
            visit.seeker  = request.user
            visit.listing = listing
            visit.save()
            send_visit_request_email.delay(visit.id)
            messages.success(request, 'Visit request sent successfully!')
            return redirect('visits:my_visits')
    else:
        form = VisitRequestForm()

    # Get available dates for this listing
    availabilities = Availability.objects.filter(
        listing      = listing,
        is_available = True,
        date__gte    = __import__('datetime').date.today()
    )

    return render(request, 'visits/request.html', {
        'form'          : form,
        'listing'       : listing,
        'availabilities': availabilities,
    })

@login_required
def my_visits(request):
    """Seeker sees their visit requests"""
    if not request.user.is_seeker():
        return redirect('dashboard')

    visits = VisitRequest.objects.filter(
        seeker=request.user
    ).select_related('listing', 'listing__owner')

    return render(request, 'visits/my_visits.html', {'visits': visits})

@login_required
def manage_visits(request):
    """Owner manages visit requests for their listings"""
    if not request.user.is_owner():
        return redirect('dashboard')

    visits = VisitRequest.objects.filter(
        listing__owner = request.user
    ).select_related('seeker', 'listing')

    return render(request, 'visits/manage.html', {'visits': visits})

@login_required
def update_visit_status(request, pk, action):
    """Owner accepts or declines a visit"""
    visit = get_object_or_404(
        VisitRequest,
        pk             = pk,
        listing__owner = request.user
    )

    if action == 'accept':
        visit.status = VisitRequest.Status.ACCEPTED
        messages.success(request, f'Visit request from {visit.seeker.username} accepted.')
        send_visit_accepted_email.delay(visit.id)
    elif action == 'decline':
        visit.status = VisitRequest.Status.DECLINED
        messages.info(request, f'Visit request from {visit.seeker.username} declined.')
        send_visit_declined_email.delay(visit.id)
    visit.save()

    if request.htmx:
        return render(request, 'visits/partials/visit_card.html', {'visit': visit})

    return redirect('visits:manage')

@login_required
def cancel_visit(request, pk):
    """Seeker cancels their visit request"""
    visit = get_object_or_404(
        VisitRequest,
        pk     = pk,
        seeker = request.user,
        status = 'pending'
    )
    visit.status = VisitRequest.Status.CANCELLED
    visit.save()
    messages.info(request, 'Visit request cancelled.')
    return redirect('visits:my_visits')

@login_required
def manage_availability(request, listing_pk):
    """Owner sets available dates for a listing"""
    listing = get_object_or_404(Listing, pk=listing_pk, owner=request.user)

    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            avail         = form.save(commit=False)
            avail.owner   = request.user
            avail.listing = listing
            avail.save()
            messages.success(request, 'Availability updated.')
            return redirect('visits:availability', listing_pk=listing_pk)
    else:
        form = AvailabilityForm()

    availabilities = Availability.objects.filter(listing=listing)

    return render(request, 'visits/availability.html', {
        'form'          : form,
        'listing'       : listing,
        'availabilities': availabilities,
    })