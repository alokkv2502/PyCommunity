import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import devsearch.routing  # Make sure this import is working

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devsearch.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Django's ASGI application to handle traditional HTTP requests
    "websocket": AuthMiddlewareStack(  # Django's ASGI application to handle WebSocket connections
        URLRouter(
            devsearch.routing.websocket_urlpatterns  # The WebSocket routing defined in devsearch/routing.py
        )
    ),
})
