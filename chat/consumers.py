'''import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.roomGroupName = "group_chat_gfg"
		await self.channel_layer.group_add(
			self.roomGroupName ,
			self.channel_name
		)
		await self.accept()
	async def disconnect(self , close_code):
		await self.channel_layer.group_discard(
			self.roomGroupName , 
			self.channel_layer 
		)
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json["message"]
		username = text_data_json["username"]
		await self.channel_layer.group_send(
			self.roomGroupName,{
				"type" : "sendMessage" ,
				"message" : message , 
				"username" : username ,
			})
	async def sendMessage(self , event) : 
		message = event["message"]
		username = event["username"]
		await self.send(text_data = json.dumps({"message":message ,"username":username}))'''

'''import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name  # Use self.channel_name instead of self.channel_layer
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.roomGroupName,{
                "type": "sendMessage",
                "message": message,
                "username": username,
            }
        )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
'''
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_chat_gfg"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

        # Send the previous messages to the user when they join
        await self.send_previous_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if "delete_id" in text_data_json:
            delete_id = text_data_json["delete_id"]
            await self.delete_message(delete_id)
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "deleteMessage",
                    "delete_id": delete_id,
                }
            )
        else:
            message = text_data_json["message"]
            username = text_data_json["username"]

            chat_message = await self.save_message(username, message)

            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "sendMessage",
                    "message": message,
                    "username": username,
                    "id": chat_message.id
                }
            )

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        message_id = event["id"]
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
            "id": message_id
        }))

    async def deleteMessage(self, event):
        delete_id = event["delete_id"]
        await self.send(text_data=json.dumps({"delete_id": delete_id}))

    @sync_to_async
    def save_message(self, username, message):
        chat_message = ChatMessage.objects.create(username=username, message=message)
        return chat_message

    @sync_to_async
    def delete_message(self, message_id):
        ChatMessage.objects.filter(id=message_id).delete()

    @sync_to_async
    def get_previous_messages(self):
        # Fetch last 10 messages
        return list(ChatMessage.objects.order_by("-timestamp")[:10].values("username", "message"))

    async def send_previous_messages(self):
        messages = await self.get_previous_messages()
        await self.send(text_data=json.dumps({"previous_messages": messages}))
