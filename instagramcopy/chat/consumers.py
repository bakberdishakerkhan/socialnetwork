import json
import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Chat
from asgiref.sync import sync_to_async

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.other_user_id = int(self.scope['url_route']['kwargs']['user_id_2'])
        self.room_name = f'chat_{min(self.user_id, self.other_user_id)}_{max(self.user_id, self.other_user_id)}'
        
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()
        

        messages = await self.get_chat_history()
        for msg in messages:
            await self.send(text_data=json.dumps({
                'message': msg.content,
                'sender_id': msg.sender.id,
                'sender_name': await self.get_display_name(msg.sender),
                'timestamp': str(msg.timestamp),
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data['message']
            
            chat_message = await self.save_message(message)
            

            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender_id': self.user_id,
                    'sender_name': await self.get_display_name(self.scope['user']),
                    'timestamp': str(datetime.datetime.now())
                }
            )
        except Exception as e:
            print("Ошибка:", e)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))


    @sync_to_async
    def get_chat_history(self):
        return list(Chat.objects.filter(
            sender_id__in=[self.user_id, self.other_user_id],
            receiver_id__in=[self.user_id, self.other_user_id]
        ).order_by('timestamp').select_related('sender'))

    @sync_to_async
    def save_message(self, message):
        sender = User.objects.get(id=self.user_id)
        receiver = User.objects.get(id=self.other_user_id)
        return Chat.objects.create(
            sender=sender,
            receiver=receiver,
            content=message
        )

    @sync_to_async
    def get_display_name(self, user):

        if user.get_full_name().strip():
            return user.get_full_name()
        return user.username.split('@')[0]