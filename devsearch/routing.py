# your_app/routing.py
from django.urls import path
from ..projects.consumers import PythonTerminalConsumer

websocket_urlpatterns = [
    path('ws/terminal/', PythonTerminalConsumer.as_asgi()),
]
