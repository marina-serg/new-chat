from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import SignUpForm, LoginForm, UpdateProfileForm, UpdateUserForm

User = get_user_model()


class SignUpFormTests(TestCase):

    def test_signup_form_valid(self):
        form_data = {
            'username': 'test_user',
            'email': 'testuser@yandex.ru',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'phone_number': '+72345678901'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.email, 'testuser@yandex.ru')
        self.assertEqual(user.phone_number, '+72345678901')

    def test_signup_form_password_mismatch(self):
        form_data = {
            'username': 'test_user',
            'email': 'testuser@yandex.ru',
            'password1': 'strongpassword123',
            'password2': 'differentpassword',
            'phone_number': '+12345678901'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_signup_form_invalid_phone_number(self):
        form_data = {
            'username': 'test_user',
            'email': 'testuser@yandex.ru',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'phone_number': '1234567801'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class LoginFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123'
        )

    def test_login_form_valid(self):
        form_data = {
            'email': 'testuser@yandex.ru',
            'password': 'strongpassword123'
        }
        form = LoginForm(data=form_data)

        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_login_form_invalid_email(self):
        form_data = {
            'email': 'wrongemail@.ru',
            'password': 'strongpassword123'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_login_form_invalid_password(self):
        form_data = {
            'email': 'testuser@yandex.ru',
            'password': 'strong'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_login_form_email_required(self):
        form_data = {
            'password': 'strongpassword123'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_login_form_password_required(self):
        form_data = {
            'email': 'testuser@yandex.ru'
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password', form.errors)


class UpdateUserFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123'
        )

    def test_update_user_form_valid(self):
        form_data = {
            'username': 'newusername',
            'email': 'newuser@yandex.ru'
        }
        form = UpdateUserForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        updated_user = form.save()
        self.assertEqual(updated_user.username, 'newusername')
        self.assertEqual(updated_user.email, 'newuser@yandex.ru')

    def test_update_user_form_invalid_email(self):
        form_data = {
            'username': 'newusername',
            'email': 'invalidemail'
        }
        form = UpdateUserForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_update_user_form_missing_fields(self):
        form_data = {
            'username': '',
            'email': ''
        }
        form = UpdateUserForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('email', form.errors)


class UpdateProfileFormTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        self.profile = self.user.profile

    def test_update_profile_form_valid(self):
        form_data = {
            'avatar': None,
            'bio': 'Test bio.'
        }
        form = UpdateProfileForm(instance=self.profile, data=form_data)
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.bio, 'Test bio.')

    def test_update_profile_form_invalid_bio(self):
        form_data = {
            'avatar': None,
            'bio': ''
        }
        form = UpdateProfileForm(instance=self.profile, data=form_data)
        self.assertTrue(form.is_valid())
