from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chat.models import Group, Message

User = get_user_model()


class URLTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        self.user.is_verified = True
        self.user.save()
        self.client.login(email='testuser@yandex.ru',
                          password='strongpassword123')

        self.group = Group.objects.create(name='Test Group')
        self.group.members.add(self.user)

    def test_home_view_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_group_chat_view_url(self):
        response = self.client.get(reverse('group', args=[self.group.uuid]))
        self.assertEqual(response.status_code, 200)

    def test_clear_chat_url(self):
        self.message1 = Message.objects.create(group=self.group, author=self.user, content='Message 1')
        response = self.client.post(reverse('clear_chat', args=[self.group.uuid]))
        self.assertEqual(self.group.message_set.count(), 0)
