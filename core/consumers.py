import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from apps.website.models import Room, Message, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_slug']
        self.roomGroupName = 'chat_%s' % self.room_name
        try:
            await self.channel_layer.group_add(
                self.roomGroupName,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            print(e)

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.roomGroupName,
                self.channel_name
            )
        except Exception as e:
            print(e)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            username = text_data_json["username"]
            room_slug = text_data_json["room_slug"]

            await self.save_message(message, username, room_slug)

            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "sendMessage",
                    "message": message,
                    "username": username,
                    "room_slug": room_slug,
                }
            )
        except Exception as e:
            print(e)

    async def sendMessage(self, event):
        try:
            message = event["message"]
            username = event["username"]
            await self.send(text_data=json.dumps({"message": message, "username": username}))
        except Exception as e:
            print(e)

    @sync_to_async
    def save_message(self, message, username, room_slug):
        try:
            print(username, room_slug, "----------------------")
            user = User.objects.get(username=username)
            room = Room.objects.get(slug=room_slug)

            Message.objects.create(user=user, room=room, content=message)
        except Exception as e:
            print(e)
