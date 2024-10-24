import time

from django.contrib.auth import get_user_model
from django.test import TestCase

from chat.models import Group, Message, Event

User = get_user_model()


class GroupModelTests(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(
            email='testuser1@yandex.ru',
            password='strong1password123',
        )

        self.user_1.phone_number = '+72345678907'
        self.user_1.save()
        self.user_2 = User.objects.create_user(
            email='testuser2@yandex.ru',
            password='strong2password123',

        )

        self.user_2.phone_number = '+72345678901'
        self.user_2.save()

        self.group = Group.objects.create(name='Test Group')

    def test_group_creation(self):
        self.assertEqual(self.group.name, 'Test Group')
        self.assertEqual(self.group.members.count(), 0)

    def test_invite_user(self):
        self.group.invite_user(self.user_1)
        self.assertIn(self.user_1, self.group.invited_users.all())

    def test_add_user_to_group(self):
        self.group.add_user_to_group(self.user_1)
        self.assertIn(self.user_1, self.group.members.all())

    def test_remove_user_from_group(self):
        self.group.add_user_to_group(self.user_1)
        self.group.remove_user_from_group(self.user_1)
        self.assertNotIn(self.user_1, self.group.members.all())

    def test_get_last_message(self):
        message_1 = Message.objects.create(group=self.group, content='Test', author=self.user_1)
        time.sleep(1)
        message_2 = Message.objects.create(group=self.group, content='Test_new', author=self.user_2)
        last_message = self.group.get_last_message()
        self.assertEqual(last_message, message_2)


class EventModelTests(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(
            email='testuser1@yandex.ru',
            password='strong1password123',
        )

        self.user_1.phone_number = '+72345678907'
        self.user_1.save()
        self.user_2 = User.objects.create_user(
            email='testuser2@yandex.ru',
            password='strong2password123',

        )

        self.user_2.phone_number = '+72345678901'
        self.user_2.save()
        self.group = Group.objects.create(name='Test Group')

    def test_event_creation_join(self):
        event = Event.objects.create(type='Join', user=self.user_1, group=self.group)
        self.assertEqual(event.description, f"{str(self.user_1)} Join the Test Group group")
        self.assertEqual(event.type, 'Join')
        self.assertEqual(event.user, self.user_1)
        self.assertEqual(event.group, self.group)

    def test_event_creation_left(self):
        event = Event.objects.create(type='Left', user=self.user_2, group=self.group)
        self.assertEqual(event.description, f"{str(self.user_2)} Left the Test Group group")
        self.assertEqual(event.type, 'Left')
        self.assertEqual(event.user, self.user_2)
        self.assertEqual(event.group, self.group)

    def test_event_str_method(self):
        event = Event.objects.create(type='Join', user=self.user_1, group=self.group)
        self.assertEqual(str(event), f"{str(self.user_1)} Join the Test Group group")

    def test_event_timestamp(self):
        event = Event.objects.create(type='Join', user=self.user_1, group=self.group)
        self.assertIsNotNone(event.timestamp)
