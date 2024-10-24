from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chat.models import Group, Message

User = get_user_model()


class HomeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123',
        )

        self.user.phone_number = '+72345678888'
        self.user.save()
        self.other_user = User.objects.create_user(
            email='othertestuser@yandex.ru',
            password='otherstrongpassword123',

        )

        self.other_user.phone_number = '+72345678777'
        self.other_user.save()
        self.client.login(email='testuser@yandex.ru',
                          password='strongpassword123')

        self.group = Group.objects.create(name='Test Group')
        self.group.members.add(self.user)

        self.message = Message.objects.create(group=self.group, author=self.user, content='Test')

    def test_home_view_for_member(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_for_invited_user(self):
        self.group.invited_users.add(self.other_user)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)

    def test_group_exited_user(self):
        self.group.exited_users.add(self.other_user)
        self.assertEqual(self.group.exited_users.count(), 1)
        last_message = self.group.get_last_message()
        self.assertEqual(last_message, self.message)


class GroupChatViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@yandex.ru',
            password='strongpassword123',
        )

        self.user.phone_number = '+72345678888'
        self.user.save()

        self.other_user = User.objects.create_user(
            email='othertestuser@yandex.ru',
            password='otherstrongpassword123',

        )
        self.other_user.save()
        self.other_user.phone_number = '+72345678777'

        self.group = Group.objects.create(name='Test Group')
        self.group.members.add(self.user)

        self.message = Message.objects.create(group=self.group, author=self.user, content='Test')

    def test_group_chat_view_access_for_non_member(self):
        self.client.login(email='othertestuser@yandex.ru',
                          password='otherstrongpassword123')
        response = self.client.get(reverse('group', args=[self.group.uuid]))
        self.assertEqual(response.status_code, 403)

    def test_update_group_info(self):
        self.client.login(email='testuser@yandex.ru',
                          password='strongpassword123')

        response = self.client.post(reverse('group', args=[self.group.uuid]), {
            'name': 'Updated Group Name'
        })

        self.group.refresh_from_db()
        self.assertEqual(response.status_code, 200)

    def test_invite_nonexistent_user(self):
        response = self.client.post(reverse('invite_user', args=[self.group.uuid]), {
            'email': 'nonexistent@yandex.ru'
        })
        self.assertEqual(response.status_code, 302)
        response = self.client.get(response.url)
        self.assertTrue(response, 'Пользователь с таким email не найден.')
