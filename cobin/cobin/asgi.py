"""
ASGI config for cobin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import cobin_app.routing  # WebSocket URL을 여기에 연결

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cobin.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # 기존 HTTP 요청 처리
    "websocket": URLRouter(cobin_app.routing.websocket_urlpatterns),  # WebSocket URL 연결
})

application = get_asgi_application()
