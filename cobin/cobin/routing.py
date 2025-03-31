from django.urls import re_path
from .consumers import PointConsumer, TradingConsumer

websocket_urlpatterns = [
    re_path(r'ws/points/(?P<user_id>\w+)/$', PointConsumer.as_asgi()),
    re_path(r'ws/trading/$', TradingConsumer.as_asgi()),
]