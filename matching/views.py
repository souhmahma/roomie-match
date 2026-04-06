from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from listings.models import Listing
from .utils import calculate_score, get_score_label, get_score_color
from .models import CompatibilityScore

@login_required
def best_matches(request):
    """Show listings sorted by compatibility score for the seeker"""
    if not request.user.is_seeker():
        return redirect('dashboard')

    try:
        profile  = request.user.seeker_profile
    except Exception:
        return redirect('profile')

    listings = Listing.objects.filter(status='active').prefetch_related('photos')

    # Calculate and attach score to each listing
    scored_listings = []
    for listing in listings:
        score = calculate_score(profile, listing)

        # Save/update score in DB
        CompatibilityScore.objects.update_or_create(
            seeker  = request.user,
            listing = listing,
            defaults = {'score': score}
        )

        listing.score       = score
        listing.score_label = get_score_label(score)
        listing.score_color = get_score_color(score)
        scored_listings.append(listing)

    # Sort by score descending
    scored_listings.sort(key=lambda x: x.score, reverse=True)

    paginator   = Paginator(scored_listings, 9)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)

    return render(request, 'matching/best_matches.html', {
        'page_obj': page_obj,
    })