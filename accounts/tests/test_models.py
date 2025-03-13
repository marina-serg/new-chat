from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class AccountsModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='example2@yandex.ru',
            password='example2password',
        )
        self.profile = self.user.profile

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'example2@yandex.ru')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_profile_creation(self):
        self.assertEqual(self.profile.bio, '')
        self.assertEqual(self.profile.user, self.user)

    def test_profile_bio_update(self):
        self.profile.bio = 'This is a bio.'
        self.profile.save()
        self.assertEqual(self.profile.bio, 'This is a bio.')

    def test_profile_avatar_default(self):
        self.assertEqual(self.profile.avatar.name, 'default.png')
