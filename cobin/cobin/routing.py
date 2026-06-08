from django.urls import re_path
from cobin.consumers import TradingConsumer, PointConsumer, ChartConsumer, ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/points/(?P<username>\w+)/$', PointConsumer.as_asgi()),
    re_path(r'ws/trading/$', TradingConsumer.as_asgi()),
    re_path(r'ws/chart/$', ChartConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<code>\w+-\w+)/$', ChatConsumer.as_asgi()),
]
