from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, SeekerProfile, OwnerProfile
from listings.models import Listing
from visits.models import VisitRequest

class TestVisits(TestCase):

    def setUp(self):
        self.client = Client()
        self.owner  = User.objects.create_user(
            username = 'owner',
            password = 'TestPass123!',
            role     = 'owner'
        )
        self.seeker = User.objects.create_user(
            username = 'seeker',
            password = 'TestPass123!',
            role     = 'seeker'
        )
        SeekerProfile.objects.create(user=self.seeker)
        OwnerProfile.objects.create(user=self.owner)

        self.listing = Listing.objects.create(
            owner          = self.owner,
            title          = 'Test room',
            description    = 'desc',
            city           = 'Paris',
            price          = 500,
            size           = 12,
            room_type      = 'private',
            status         = 'active',
            available_from = '2026-01-01',
        )

    def test_seeker_can_request_visit(self):
        self.client.login(username='seeker', password='TestPass123!')
        response = self.client.post(
            reverse('visits:request', args=[self.listing.pk]), {
                'date'   : '2026-06-01',
                'time'   : '14:00',
                'message': 'Hello!',
            }
        )
        self.assertEqual(VisitRequest.objects.count(), 1)
        visit = VisitRequest.objects.first()
        self.assertEqual(visit.status, 'pending')

    def test_owner_can_accept_visit(self):
        visit = VisitRequest.objects.create(
            seeker  = self.seeker,
            listing = self.listing,
            date    = '2026-06-01',
            time    = '14:00',
            status  = 'pending'
        )
        self.client.login(username='owner', password='TestPass123!')
        self.client.post(reverse('visits:update_status', args=[visit.pk, 'accept']))
        visit.refresh_from_db()
        self.assertEqual(visit.status, 'accepted')

    def test_duplicate_visit_request_blocked(self):
        self.client.login(username='seeker', password='TestPass123!')
        # First request
        self.client.post(
            reverse('visits:request', args=[self.listing.pk]), {
                'date': '2026-06-01',
                'time': '14:00',
            }
        )
        # Second request — should be blocked
        self.client.post(
            reverse('visits:request', args=[self.listing.pk]), {
                'date': '2026-06-02',
                'time': '15:00',
            }
        )
        self.assertEqual(VisitRequest.objects.count(), 1)