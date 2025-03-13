import unittest

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model

from chat.models import Group
from chat.consumers import JoinAndLeave, GroupConsumer, UserSearchConsumer

User = get_user_model()


class RoutingTests(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        await database_sync_to_async(User.objects.all().delete)()
        self.user = await database_sync_to_async(User.objects.create_user)(
            username='testuser',
            email='testuser@yandex.ru',
            password='strongpassword123'
        )
        self.user.is_verified = True
        await database_sync_to_async(self.user.save)()



        self.group = await database_sync_to_async(Group.objects.create)(name='Test Group')

    async def asyncTearDown(self):
        await database_sync_to_async(self.user.delete)()

    async def test_join_leave_routing(self):
        communicator = WebsocketCommunicator(JoinAndLeave.as_asgi(), "/ws/join_leave/")
        communicator.scope['user'] = self.user
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.disconnect()



    async def test_user_search_routing(self):
        communicator = WebsocketCommunicator(UserSearchConsumer.as_asgi(),
                                             f"/ws/search_users/groups/{self.group.uuid}/")
        communicator.scope['user'] = self.user
        communicator.scope['url_route'] = {
            'kwargs': {
                'uuid': str(self.group.uuid)}}
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.disconnect()
