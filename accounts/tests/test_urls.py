from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class URLTests(TestCase):

    def test_register_url(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_my_profile_url(self):
        response = self.client.get(reverse('user_detail', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 302)

    def test_password_change_url(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 302)

    def test_password_reset_url(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_url(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_url(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
