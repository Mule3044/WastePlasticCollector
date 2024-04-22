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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WastePlasticCollector.settings')

# application = get_asgi_application()
# 👇 2. Update the application var
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
            URLRouter(
                websocket_urlpatterns
            )
        ),
})
# import os
# from django.core.asgi import get_asgi_application
# from django.core.wsgi import get_wsgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from WastePlasticCollectorApp.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WastePlasticCollector.settings')

# # Get the Django ASGI application
# django_asgi_application = get_asgi_application()

# # Get the Django WSGI application
# django_wsgi_application = get_wsgi_application()

# # Define the WebSocket routing
# websocket_application = ProtocolTypeRouter({
#     "http": django_asgi_application,
#     "websocket": AllowedHostsOriginValidator(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })

# # Define the combined ASGI application
# application = ProtocolTypeRouter({
#     "http": django_wsgi_application,
#     "websocket": websocket_application,
# })

