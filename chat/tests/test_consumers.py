import unittest

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model

from chat.consumers import JoinAndLeave
from chat.models import Group, Message

User = get_user_model()


class JoinAndLeaveConsumerTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await database_sync_to_async(User.objects.all().delete)()
        self.user = await database_sync_to_async(User.objects.create_user)(
            username='testuser',
            email='example2@yandex.ru',
            password='example2password',
        )
        self.user.is_verified=True



        self.user.asave()

        self.group = await Group.objects.acreate(name='Test Group')

        self.communicator = WebsocketCommunicator(JoinAndLeave.as_asgi(), "/ws/join_leave/")
        self.communicator.scope['user'] = self.user

        self.connected, _ = await self.communicator.connect()

    async def asyncTearDown(self):
        await self.communicator.disconnect()

    async def test_join_group(self):
        await self.communicator.send_json_to({
            "type": "join_group",
            "data": str(self.group.uuid)})

        response = await self.communicator.receive_json_from()

        self.assertEqual(response['type'], 'join_group')
        self.assertEqual(response['data'], str(self.group.uuid))

        members = await database_sync_to_async(list)(self.group.members.all())
        self.assertIn(self.user, members)

    async def test_leave_group(self):
        await self.communicator.send_json_to({
            "type": "leave_group",
            "data": str(self.group.uuid)})

        response = await self.communicator.receive_json_from()

        self.assertEqual(response['type'], 'leave_group')
        self.assertEqual(response['data']['group_uuid'], str(self.group.uuid))
        group_exists = await database_sync_to_async(Group.objects.filter(uuid=self.group.uuid).exists)()
        self.assertFalse(group_exists)



class GroupConsumerTest(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await database_sync_to_async(User.objects.all().delete)()
        self.user = await database_sync_to_async(User.objects.create_user)(
            username='testuser',
            email='example2@yandex.ru',
            password='example2password',
        )
        self.user.is_verified=True



        await database_sync_to_async(self.user.save)()

        self.group = await Group.objects.acreate(name='Test Group')
        await database_sync_to_async(self.group.members.add)(self.user)
        self.communicator = WebsocketCommunicator(JoinAndLeave.as_asgi(), f"/groups/{self.group.uuid}/")
        self.communicator.scope['user'] = self.user
        self.connected, _ = await self.communicator.connect()

    async def asyncTearDown(self):
        await self.communicator.disconnect()

    async def test_connect(self):
        self.assertTrue(self.connected)

    async def test_send_text_message(self):
        message_data = {
            "type": "text_message",
            "message": "Test message",
            "author": self.user.email,
        }

        await self.communicator.send_json_to(message_data)
        message_exists = await database_sync_to_async(Message.objects.filter(content='Test message').exists)()
        self.assertFalse(message_exists)
