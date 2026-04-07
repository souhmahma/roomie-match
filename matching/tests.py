from django.test import TestCase
from accounts.models import User, SeekerProfile
from listings.models import Listing
from matching.utils import calculate_score

class TestMatchingAlgorithm(TestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username = 'owner',
            password = 'pass',
            role     = 'owner'
        )
        self.seeker = User.objects.create_user(
            username = 'seeker',
            password = 'pass',
            role     = 'seeker'
        )
        self.profile = SeekerProfile.objects.create(
            user        = self.seeker,
            budget_min  = 400,
            budget_max  = 700,
            schedule    = 'normal',
            noise_level = 'medium',
            has_pets    = False,
            is_smoker   = False,
            is_student  = False,
        )
        self.listing = Listing.objects.create(
            owner               = self.owner,
            title               = 'Perfect room',
            description         = 'desc',
            city                = 'Paris',
            price               = 600,
            size                = 15,
            room_type           = 'private',
            status              = 'active',
            available_from      = '2026-01-01',
            preferred_schedule  = 'normal',
            preferred_noise     = 'medium',
            pets_allowed        = True,
            smoking_allowed     = False,
            students_allowed    = True,
        )

    def test_perfect_score(self):
        score = calculate_score(self.profile, self.listing)
        self.assertEqual(score, 100)

    def test_budget_too_high(self):
        self.listing.price = 900  # above budget
        self.listing.save()
        score = calculate_score(self.profile, self.listing)
        self.assertLess(score, 100)

    def test_score_range(self):
        score = calculate_score(self.profile, self.listing)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

    def test_smoker_mismatch(self):
        self.profile.is_smoker = True
        self.profile.save()
        self.listing.smoking_allowed = False
        self.listing.save()
        score = calculate_score(self.profile, self.listing)
        self.assertLess(score, 100)