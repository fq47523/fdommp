from django.urls import path,re_path
from webssh.tools.channel import websocket
from hosts.comsumers import AnsibleModel

websocket_urlpatterns = [
    path('webssh/', websocket.WebSSH),
    re_path('ansible/model/(?P<group_name>.*)/', AnsibleModel),
]
