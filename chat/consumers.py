import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from accounts.models import User
from .models import Message, Group


class JoinAndLeave(AsyncWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["user"]
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        if type:
            data = text_data.get("data", None)

        if type == "leave_group":
            await self.leave_group(data)
        elif type == "join_group":
            await self.join_group(data)
        elif type == "delete_group":
            await self.delete_group(data)

    async def leave_group(self, group_uuid):
        group = await Group.objects.aget(uuid=group_uuid)

        await database_sync_to_async(group.remove_user_from_group)(self.user)

        members_count = await group.members.acount()
        data = {
            "type": "leave_group",
            "data": {
                "group_uuid": group_uuid,
                "members_count": members_count
            }
        }

        await self.send(json.dumps(data))

        if members_count == 0:
            await database_sync_to_async(group.delete)()
        else:
            await database_sync_to_async(group.exited_users.add)(self.user)

    async def join_group(self, group_uuid):
        group = await Group.objects.aget(uuid=group_uuid)
        await database_sync_to_async(group.add_user_to_group)(self.user)
        data = {
            "type": "join_group",
            "data": group_uuid
        }
        await self.send(json.dumps(data))

    async def delete_group(self, group_uuid):
        try:
            group = await Group.objects.aget(uuid=group_uuid)
            await database_sync_to_async(group.exited_users.remove)(self.user)
            await database_sync_to_async(group.invited_users.remove)(self.user)
            await group.asave()
        except Group.DoesNotExist:
            pass

        data = {
            "type": "delete_group",
            "data": group_uuid
        }
        await self.send(json.dumps(data))


@database_sync_to_async
def get_messages(message, group):
    return Message.objects.filter(content__icontains=message, group=group)


@database_sync_to_async
def convert_messages_to_dict(messages):
    return [{"message_id": msg.id, "text": msg.content, "author": str(msg.author.email)} for msg in messages]


@database_sync_to_async
def search(query, group_uuid):
    group = Group.objects.get(uuid=group_uuid)
    members = list(group.members.values_list('id', flat=True))
    invited_users = list(group.invited_users.values_list('id', flat=True))
    return User.objects.filter(email__icontains=query).exclude(id__in=members + invited_users)


@database_sync_to_async
def users_convert(users):
    return [str(user.email) for user in users]


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        self.group = await Group.objects.aget(uuid=self.group_uuid)
        await self.channel_layer.group_add(self.group_uuid, self.channel_name)

        self.user = self.scope["user"]
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        group = self.group
        if type == "text_message":
            await self.handle_text_message(text_data)
        elif type == "search_message":
            await self.handle_search_message(text_data, group)

    async def handle_text_message(self, text_data):
        message = text_data.get("message", None)
        author = text_data.get("author", None)
        user = await User.objects.aget(email=author)
        new_message = await Message.objects.acreate(
            author=user,
            content=message,
            group=self.group
        )
        await self.channel_layer.group_send(
            self.group_uuid,
            {
                "type": "text_message",
                "message": str(new_message),
                "author": author,
            }
        )

    async def handle_search_message(self, text_data, group):
        message = text_data.get("message", None)
        messages = await get_messages(message, group)
        messages_dict = await convert_messages_to_dict(messages)
        await self.channel_layer.group_send(
            self.group_uuid,
            {
                "type": "search_message",
                "message": messages_dict,
                "author": text_data.get("author", None),
            }
        )

    async def text_message(self, event):
        await self.send(json.dumps(event))

    async def search_message(self, event):
        await self.send(json.dumps(event))


class UserSearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_uuid = str(self.scope["url_route"]["kwargs"]["uuid"])
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        query = data.get('query', '')
        users = await search(query, self.group_uuid)
        users_list = await users_convert(users)

        await self.send(text_data=json.dumps({
            'type': 'user_search',
            'users': users_list
        }))
