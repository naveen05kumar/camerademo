import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_detection.settings')

# Import settings after setting the DJANGO_SETTINGS_MODULE
from django.conf import settings

django_asgi_app = get_asgi_application()

# Ensure Django apps are loaded before importing routing
apps.populate(settings.INSTALLED_APPS)

from camera import routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})