from django.urls import path
from webssh.tools.channel import websocket

websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
]
