from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Profile

User = get_user_model()


class ProfileSignalTests(TestCase):

    def test_create_profile_on_user_creation(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(profile)

        self.assertEqual(profile.user, self.user)
