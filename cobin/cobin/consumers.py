import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import websockets

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


class PointConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.group_name = f"user_{self.username}"

        # WebSocket 연결 수락
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # WebSocket 연결 해제
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_point_update(self, event):
        # 클라이언트로 메시지 전송
        await self.send(text_data=json.dumps(event['message']))
        
class ChartConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        asyncio.create_task(self.upbit_ws())

    async def upbit_ws(self):
        url = "wss://api.upbit.com/websocket/v1"
        async with websockets.connect(url) as websocket:
            subscribe_fmt = [
                {"ticket": "test"},
                {
                    "type": "ticker",
                    "codes": ["KRW-BTC"],  # 여기서 코인 종류 지정 (BTC/USDT면 "USDT-BTC")
                },
                {"format": "SIMPLE"}
            ]
            await websocket.send(json.dumps(subscribe_fmt))

            while True:
                data = await websocket.recv()
                data_json = json.loads(data)
                price = data_json['tp']  # 체결가격

                await self.send(text_data=json.dumps({
                    'price': price
                }))