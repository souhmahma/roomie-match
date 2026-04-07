import pytest
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, SeekerProfile, OwnerProfile

class TestUserRegistration(TestCase):

    def setUp(self):
        self.client = Client()

    def test_register_seeker(self):
        response = self.client.post(reverse('register'), {
            'username' : 'testseeker',
            'email'    : 'seeker@test.com',
            'role'     : 'seeker',
            'city'     : 'Paris',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testseeker')
        self.assertEqual(user.role, 'seeker')
        self.assertTrue(hasattr(user, 'seeker_profile'))

    def test_register_owner(self):
        response = self.client.post(reverse('register'), {
            'username' : 'testowner',
            'email'    : 'owner@test.com',
            'role'     : 'owner',
            'city'     : 'Lyon',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testowner')
        self.assertEqual(user.role, 'owner')
        self.assertTrue(hasattr(user, 'owner_profile'))

    def test_login(self):
        User.objects.create_user(
            username = 'loginuser',
            password = 'TestPass123!',
            role     = 'seeker'
        )
        response = self.client.post(reverse('login'), {
            'username': 'loginuser',
            'password': 'TestPass123!',
        })
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)