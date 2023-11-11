import json
from django.contrib.auth.models import User #for getting the user model

from channels.generic.websocket import AsyncWebsocketConsumer #for creating a websocket consumer
from asgiref.sync import sync_to_async  #for querying the database asynchronously

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name'] #get the room name from the url
        self.chatroom_group_name = 'chat_%s' % self.chatroom_name #create a group name for the room

        # Join room group
        await self.channel_layer.group_add(
            self.chatroom_group_name,
            self.channel_name
        )
        #accept the connection
        await self.accept()

    async def disconnect(self):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chatroom_group_name,
            self.channel_name
        )
    #receive message from websocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        chatroom = data['chatroom']
        
        #save the message to the database
        
        await self.save_message(username, chatroom, message)
        #send the message to the group
        await self.channel_layer.group_send(
            self.chatroom_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'chatroom': chatroom,
            }
        )
    #receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        chatroom = event['chatroom']
        #send message to the websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'chatroom': chatroom,
        }))
    #save message to the database
