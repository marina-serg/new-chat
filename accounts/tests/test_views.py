from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class RegisterViewTests(TestCase):

    def setUp(self):
        self.url = reverse('register')

    def test_register_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_signup_form_valid(self):
        response = self.client.post(self.url, {
            'username': 'test_user',
            'email': 'testuser@yandex.ru',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertRedirects(response, '/accounts/confirm_email/')
        self.assertTrue(User.objects.filter(username='test_user').exists())


class ProfileViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        self.user.is_verified = True
        self.user.save()
        self.profile = self.user.profile

    def test_profile_view_post_valid_data(self):
        self.client.login(username='testuser@yandex.ru', password='strongpassword123')
        form_data = {
            'username': 'newusername',
            'last_name': 'newlastname',
            'first_name': 'newfirstname',
        }
        profile_data = {
            'bio': 'Updated bio.'
        }
        response = self.client.post(reverse('edit'), data={**form_data, **profile_data})

        self.user.refresh_from_db()
        self.profile.refresh_from_db()

        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.last_name, 'newlastname')
        self.assertEqual(self.user.first_name, 'newfirstname')
        self.assertEqual(self.profile.bio, 'Updated bio.')

    def test_profile_view_post_invalid_data(self):
        self.client.login(username='testuser@yandex.ru', password='strongpassword123')

        form_data = {
            'username': ''
        }
        profile_data = {
            'bio': 'Updated bio.'
        }
        response = self.client.post(reverse('edit'), data={**form_data, **profile_data})

        self.assertEqual(response.status_code, 200)

    def test_profile_view_not_logged_in(self):
        response = self.client.get(reverse('edit'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("edit")}')


class ChangePasswordViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        self.user.is_verified = True
        self.user.save()
        self.client.login(username='testuser@yandex.ru', password='strongpassword123')

    def test_change_password_view_get(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/change_password.html')

    def test_change_password_view_post_valid_data(self):
        response = self.client.post(reverse('password_change'), {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertRedirects(response, reverse('home'))

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_change_password_view_post_invalid_data(self):
        response = self.client.post(reverse('password_change'), {
            'new_password1': 'wrongpassword123',
            'new_password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user.check_password('strongpassword123'))


class CustomPasswordResetViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='testuser@yandex.ru',
            password='strongpassword123'
        )


    def test_password_reset_view_get(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')


class ProfileViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        self.user.is_verified = True
        self.user.save()

    def test_profile_view_redirects_anonymous_user(self):
        response = self.client.get(reverse('user_detail', kwargs={'username': 'testuser'}))
        self.assertRedirects(response,
                             f'/accounts/login/?next={reverse("user_detail", kwargs={"username": "testuser"})}')

    def test_profile_view_login_user(self):
        self.client.login(username='testuser@yandex.ru', password='strongpassword123')

        response = self.client.get(reverse('user_detail', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/users_detail.html')
