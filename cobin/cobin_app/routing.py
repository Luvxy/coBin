from django.urls import re_path
from .consumers import TradingConsumer

websocket_urlpatterns = [
    re_path(r'ws/trading/$', TradingConsumer.as_asgi()),  # ✅ URL이 정확한지 확인
]
