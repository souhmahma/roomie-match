def calculate_score(seeker_profile, listing):
    """
    Calculate compatibility score between a seeker and a listing.
    Returns a score between 0 and 100.
    """
    score  = 0
    total  = 0

    # --- 1. Budget (25 points) ---
    total += 25
    if listing.price <= seeker_profile.budget_max:
        if listing.price >= seeker_profile.budget_min:
            score += 25   # perfect match
        else:
            score += 15   # below budget → still ok
    # above budget → 0 points

    # --- 2. Schedule (20 points) ---
    total += 20
    if listing.preferred_schedule == seeker_profile.schedule:
        score += 20       # exact match
    elif listing.preferred_schedule == 'normal' or seeker_profile.schedule == 'normal':
        score += 10       # one is flexible

    # --- 3. Noise level (20 points) ---
    total += 20
    if listing.preferred_noise == seeker_profile.noise_level:
        score += 20       # exact match
    elif abs(
        _noise_to_int(listing.preferred_noise) -
        _noise_to_int(seeker_profile.noise_level)
    ) == 1:
        score += 10       # one level apart

    # --- 4. Pets (15 points) ---
    total += 15
    if seeker_profile.has_pets and listing.pets_allowed:
        score += 15       # seeker has pets and listing allows them
    elif not seeker_profile.has_pets:
        score += 15       # seeker has no pets → always ok

    # --- 5. Smoking (10 points) ---
    total += 10
    if seeker_profile.is_smoker and listing.smoking_allowed:
        score += 10
    elif not seeker_profile.is_smoker:
        score += 10

    # --- 6. Student (10 points) ---
    total += 10
    if seeker_profile.is_student and listing.students_allowed:
        score += 10
    elif not seeker_profile.is_student:
        score += 10

    # Convert to percentage
    return round((score / total) * 100)


def _noise_to_int(noise_level):
    """Helper — convert noise level to int for comparison"""
    mapping = {'quiet': 1, 'medium': 2, 'loud': 3}
    return mapping.get(noise_level, 2)


def get_score_label(score):
    """Return a human readable label for the score"""
    if score >= 80:
        return 'Great match'
    elif score >= 60:
        return 'Good match'
    elif score >= 40:
        return 'Moderate match'
    else:
        return 'Low match'


def get_score_color(score):
    """Return Tailwind classes for the score badge"""
    if score >= 80:
        return 'bg-green-100 text-green-700'
    elif score >= 60:
        return 'bg-yellow-100 text-yellow-700'
    elif score >= 40:
        return 'bg-orange-100 text-orange-700'
    else:
        return 'bg-red-100 text-red-700'