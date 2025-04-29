from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/points/(?P<user_id>\w+)/$', consumers.PointConsumer.as_asgi()),
    re_path(r'ws/trading/$', consumers.TradingConsumer.as_asgi()),
    re_path(r'ws/chart/$', consumers.ChartConsumer.as_asgi()),
]