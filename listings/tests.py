from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from listings.models import Listing

class TestListings(TestCase):

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
        self.listing = Listing.objects.create(
            owner          = self.owner,
            title          = 'Nice room in Paris',
            description    = 'A nice room',
            city           = 'Paris',
            price          = 600,
            size           = 15,
            room_type      = 'private',
            status         = 'active',
            available_from = '2026-01-01',
        )

    def test_listing_list_public(self):
        response = self.client.get(reverse('listings:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nice room in Paris')

    def test_listing_detail_public(self):
        response = self.client.get(reverse('listings:detail', args=[self.listing.pk]))
        self.assertEqual(response.status_code, 200)

    def test_create_listing_requires_owner(self):
        self.client.login(username='seeker', password='TestPass123!')
        response = self.client.get(reverse('listings:create'))
        self.assertEqual(response.status_code, 302)

    def test_owner_can_create_listing(self):
        self.client.login(username='owner', password='TestPass123!')
        response = self.client.post(reverse('listings:create'), {
            'title'             : 'New room',
            'description'       : 'Great room',
            'city'              : 'Lyon',
            'price'             : 500,
            'size'              : 12,
            'room_type'         : 'private',
            'available_from'    : '2026-02-01',
            'preferred_schedule': 'normal',
            'preferred_noise'   : 'medium',
            'photos-TOTAL_FORMS'  : '0',
            'photos-INITIAL_FORMS': '0',
            'photos-MIN_NUM_FORMS': '0',
            'photos-MAX_NUM_FORMS': '10',
        })
        self.assertTrue(Listing.objects.filter(title='New room').exists())