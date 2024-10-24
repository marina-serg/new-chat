from django.test import TestCase
from django.contrib.auth import get_user_model

from django.urls import reverse

User = get_user_model()


class SignUpViewTests(TestCase):

    def setUp(self):
        self.url = reverse('signup')

    def test_signup_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form_valid(self):
        response = self.client.post(self.url, {
            'username': 'test_user',
            'email': 'testuser@yandex.ru',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'phone_number': '+72345678901'
        })
        self.assertTrue(User.objects.filter(username='test_user').exists())

    def test_redirect_authenticated_user(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123'
        )

        self.client.login(email='testuser@yandex.ru',
                          password='strongpassword123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/')


class ProfileViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        self.profile = self.user.profile

    def test_profile_view_post_valid_data(self):
        self.client.login(email='testuser@yandex.ru', password='strongpassword123')
        form_data = {
            'username': 'newusername',
            'email': 'newemail@yandex.ru'
        }
        profile_data = {
            'bio': 'Updated bio.'
        }
        response = self.client.post(reverse('users-profile'), data={**form_data, **profile_data})
        self.assertRedirects(response, reverse('users-profile'))

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@yandex.ru')
        self.assertEqual(self.profile.bio, 'Updated bio.')

    def test_profile_view_post_invalid_data(self):
        self.client.login(email='testuser@yandex.ru', password='strongpassword123')

        form_data = {
            'username': '',
            'email': 'invalidemail'}
        profile_data = {
            'bio': 'Updated bio.'
        }
        response = self.client.post(reverse('users-profile'), data={**form_data, **profile_data})

        self.assertEqual(response.status_code, 200)

    def test_profile_view_not_logged_in(self):
        response = self.client.get(reverse('users-profile'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("users-profile")}')


class ChangePasswordViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='oldpassword123'
        )
        self.client.login(email='testuser@yandex.ru', password='oldpassword123')

    def test_change_password_view_get(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/change_password.html')

    def test_change_password_view_post_valid_data(self):
        response = self.client.post(reverse('password_change'), {
            'old_password': 'oldpassword123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertRedirects(response, reverse('home'))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_change_password_view_post_invalid_data(self):
        response = self.client.post(reverse('password_change'), {
            'old_password': 'wrongpassword',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password('oldpassword123'))


class CustomPasswordResetViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='oldpassword123'
        )

    def test_password_reset_view_get(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')


class ProfileViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123'
        )

    def test_profile_view_redirects_anonymous_user(self):
        response = self.client.get(reverse('my-profile'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("my-profile")}')

    def test_profile_view_login_user(self):
        self.client.login(email='testuser@yandex.ru', password='strongpassword123')

        response = self.client.get(reverse('my-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/profile_view.html')
