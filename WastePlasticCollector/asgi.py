"""
ASGI config for WastePlasticCollector project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from WastePlasticCollectorApp.routing import websocket_urlpatterns
from channels.security.websocket import OriginValidator

settings_module = 'WastePlasticCollector.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'WastePlasticCollector.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OriginValidator(
        URLRouter(websocket_urlpatterns),
        allowed_origins=['*'],
        # allowed_origins=['ws://127.0.0.1:8000', 'ws://localhost:8000'],
    ),
})





