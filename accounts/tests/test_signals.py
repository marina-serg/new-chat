from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class ProfileSignalTests(TestCase):

    def test_create_profile_on_user_creation(self):
        user = User.objects.create_user(
            username='test',
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        profile = user.profile
        self.assertIsNotNone(profile)

        self.assertEqual(profile.user, user)
        self.assertEqual(profile.bio, '')
        self.assertEqual(profile.avatar.name, 'default.png')
