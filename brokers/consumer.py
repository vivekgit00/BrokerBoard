from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import json
# from .delta_client import client_symbol_map, consumer_channels

class DeltaConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.scope["session_id"] = self.channel_name
        await self.send(text_data=json.dumps({
            "message": "connected",
            "channel": self.channel_name  # Send this to frontend to use in API
        }))
        print("consumer------->", self.channel_name)
    async def send_ltp(self, event):
        await self.send(text_data=event["text"])
