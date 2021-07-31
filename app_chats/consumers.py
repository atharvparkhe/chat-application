from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *
from app_accounts.models import Customers

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        room_obj = Room.objects.get(id = self.room_name)
        self.room_group_name = f"chat-{room_obj.name}"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data = json.dumps({'Connected' : True}))

    def receive(self , text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'send_message',
                'payload' : text_data
            }
        )
        data = json.loads(text_data)
        Chat.objects.create(
            group = Room.objects.get(id = self.room_name),
            sender = Customers.objects.get(email = data['sender']),
            message = data['message']
        )

    def disconnect(self, *args , **kwargs):
        print('Disconnected')

    def send_message(self , event):
        data = event['payload']
        data = json.loads(data)
        self.send(text_data = json.dumps({'answer' : data }))

# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
# print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")