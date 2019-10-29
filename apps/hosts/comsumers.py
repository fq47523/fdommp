from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

class AnsibleModel(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super(AnsibleModel, self).__init__(*args, **kwargs)


    def send_msg(self, msg, logId):

        self.send(text_data=msg)

        print ('send_msg:',msg,logId)

    def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print (self.group_name )
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)

        self.accept()

    def receive(self, text_data=None, bytes_data=None):

        request = json.loads(text_data)
        print (request)
        self.send(text_data="<font color='#FA8072'> {stdout} </font>".format(stdout=request['custom']))
        self.send("\n<font color='red'>执行完成，总共{count}台机器，耗时：{time}</font>".format(count=1, time=2))

        self.close()

    def record_resullt(self, user, ans_model, ans_server, ans_args):

        print (user,ans_model,ans_server,ans_args)


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()
