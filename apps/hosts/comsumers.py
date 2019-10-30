from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from api.utils.ansible_api import ANSRunner
import json

class AnsibleModel(WebsocketConsumer):
    '''test websocket sync'''
    def __init__(self, *args, **kwargs):
        super(AnsibleModel, self).__init__(*args, **kwargs)


    def send_msg(self, msg, logId):

        self.send(text_data=msg)

        print ('send_msg:',msg,logId)

    def connect(self):
        '''接受websocket 请求'''
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        print (self.group_name )
        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name) #异步使用redis建立组和通道，可以给组发消息

        self.accept()   #允许接受请求

    def receive(self, text_data=None, bytes_data=None):
        '''获取websocket请求内容'''
        request = json.loads(text_data)
        print (request)
        rbt = ANSRunner([], redisKey='1')
        rbt.run_model(host_list=[request['ip']], module_name='shell',
                      module_args='{}'.format(request['arg']))
        data = rbt.get_model_result()

        self.send(text_data="<font color='#FA8072'> {stdout} </font>".format(stdout=json.dumps(data)))
        self.send("\n<font color='red'>执行完成，总共{count}台机器，耗时：{time}</font>".format(count=1, time=2))

        self.close()

    def record_resullt(self, user, ans_model, ans_server, ans_args):

        print (user,ans_model,ans_server,ans_args)


    def disconnect(self, close_code):
        '''异步使用redis离开组和通道，可以给组发消息'''
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        self.close()
