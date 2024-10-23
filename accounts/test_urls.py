from django.test import TestCase
from django.urls import reverse


class URLTests(TestCase):
    def test_signup_url(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_url(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_my_profile_url(self):
        response = self.client.get(reverse('my-profile'))
        self.assertEqual(response.status_code, 302)

    def test_users_profile_url(self):
        response = self.client.get(reverse('users-profile'))
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

    def test_password_reset_confirm_url(self):
        response = self.client.get(
            reverse('password_reset_confirm', kwargs={'uidb64': 'dummyuid', 'token': 'dummytoken'}))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_url(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
