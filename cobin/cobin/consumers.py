import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import websockets
import time
from channels.db import database_sync_to_async

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
        self.time_unit = "minute30"  # 기본 시간 단위 설정
        self.code = "KRW-BTC"  # 기본 코인 코드 설정
        asyncio.create_task(self.upbit_ws())

    async def receive_json(self, content):
        # 클라이언트에서 시간 단위를 변경할 경우 처리
        self.time_unit = content.get("time_unit", self.time_unit)
        self.code = content.get("code", "KRW-BTC")
        print(f"Time Unit Changed: {self.time_unit}, Code: {self.code}")

    async def upbit_ws(self):
        url = "wss://api.upbit.com/websocket/v1"
        async with websockets.connect(url) as websocket:
            subscribe_fmt = [
                {"ticket": "test"},
                {
                    "type": "ticker",
                    "codes": [f"{self.code}"],  # 코인 종류 지정
                },
                {"format": "SIMPLE"}
            ]
            await websocket.send(json.dumps(subscribe_fmt))

            while True:
                data = await websocket.recv()
                data_json = json.loads(data)
                price = data_json['tp']  # 체결가격

                await self.send(text_data=json.dumps({
                    'price': price,
                    'time_unit': self.time_unit  # 현재 시간 단위도 클라이언트로 전송
                }))

class ChatConsumer(AsyncWebsocketConsumer):
    last_sent_time = 0  # 클래스 변수로 1초 간격 제한

    async def connect(self):
        self.code = self.scope['url_route']['kwargs']['code']
        self.room_group_name = f'chat_{self.code}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        messages = await self.get_recent_messages()
        
        for msg in messages:
            await self.send(text_data=json.dumps(msg))
            
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        from cobin_app.models import ChatMessage
        data = json.loads(text_data)
        username = self.scope['user'].username if self.scope['user'].is_authenticated else '익명'
        message = data['message']

        # 메시지 길이 제한
        if len(message) > 60:
            await self.send(text_data=json.dumps({
                'username': 'System',
                'message': '메시지는 최대 60자까지 가능합니다.'
            }))
            return

        current_time = time.time()
        if current_time - self.last_sent_time < 1:
            await self.send(text_data=json.dumps({
                'username': 'System',
                'message': '1초에 한 번만 전송할 수 있습니다.'
            }))
            return

        # ✅ DB 저장 (비동기)
        if self.scope['user'].is_authenticated:
            await database_sync_to_async(ChatMessage.objects.create)(
                coin_code=self.code,
                user=self.scope['user'],
                message=message
            )
        else:
            await database_sync_to_async(ChatMessage.objects.create)(
                coin_code=self.code,
                user=None,
                message=message
            )

        self.last_sent_time = current_time

        # 메시지 전송
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'username': username,
            'message': message
        })
        
    @database_sync_to_async
    def get_recent_messages(self):
        from cobin_app.models import ChatMessage
        messages = ChatMessage.objects.filter(coin_code=self.code).order_by('-timestamp')[:30][::-1]
        return [
            {
                "username": m.user.username if m.user else "익명",
                "message": m.message,
                "timestamp": m.timestamp.strftime('%H:%M')
            }
            for m in messages
        ]
        
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'username': event['username'],
            'message': event['message']
        }))