from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import (
    MyAuthenticationForm,
    RegistrationForm,
    UserEditForm,
    ProfileEditForm,
    MyPasswordResetForm,
    MySetPasswordForm,
    MyPasswordChangeForm
)

User = get_user_model()


class UserFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='strongpassword123',
            is_verified=True
        )
        self.profile = self.user.profile

    def test_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_email(self):
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'not-an-email',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_authentication_form_valid(self):
        form_data = {
            'username': 'test@example.com',
            'password': 'strongpassword123'
        }
        request = self.client.post("/login/")
        form = MyAuthenticationForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.get_user(), self.user)

    def test_authentication_form_invalid_credentials(self):
        form_data = {
            'username': 'test@example.com',
            'password': 'wrongpassword123'
        }
        request = self.client.post("/login/")
        form = MyAuthenticationForm(data=form_data, request=request)
        self.assertFalse(form.is_valid())

    def test_user_edit_form(self):
        form_data = {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        form = UserEditForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_profile_edit_form(self):
        form_data = {
            'bio': 'This is a new bio.'
        }
        form = ProfileEditForm(instance=self.profile, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'This is a new bio.')

    def test_password_reset_form_valid(self):
        form_data = {
            'email': 'test@example.com'
        }
        form = MyPasswordResetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_set_password_form(self):
        form = MySetPasswordForm(user=self.user, data={
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_password_change_form(self):
        self.client.login(username='test@example.com', password='password123')
        form = MyPasswordChangeForm(user=self.user, data={
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(self.user.check_password('newpassword123'))
