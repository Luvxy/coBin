import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TradingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(json.dumps({"message": "WebSocket 연결 성공!"}))

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received: {data}")
        await self.send(json.dumps({"message": "데이터 받음", "data": data}))

    async def disconnect(self, close_code):
        print("WebSocket 연결 종료")
