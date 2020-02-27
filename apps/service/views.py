from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from hosts import models
from assets.models import Asset
from hosts.models import Service
from dao.base import APBase
from service.modelform.service_modelform import Service_MF
from utils._BT_pagination import BtPaging
from utils._Check_service_status import ServiceHealth
from tasks.tasks import get_server_status
from api.utils.ansible_api import *


import json
# Create your views here.


@login_required
def server(request):
    '''服务首页'''


    if request.method == "GET":
        return render(request, 'service/server.html')
    if request.method == "POST":
        page_json = json.loads(request.body)
        # print (page_json)
        host_paginf_date = BtPaging(Service, page_json)
        host_paginf_date_ret = host_paginf_date.server_paging()

        return JsonResponse(host_paginf_date_ret)



@login_required
def server_add(request):
    if request.method == 'GET':
        Service_MF_I = Service_MF()
        return render(request,'service/server_add.html',locals())

    if request.method == 'POST':
        server_status = {"sts": None, "msg": None}
        s_name = request.POST.get('s_name')
        s_host_id = request.POST.getlist('h_server')
        server_add_obj = Service_MF(request.POST)

        if server_add_obj.is_valid():
            server_add_obj.save()
            server_status['sts'] = True
            server_status['rcode'] = 200

            host_ip = Asset.objects.filter(id__in=s_host_id).values('manage_ip')
            host_ip_list = [i['manage_ip'] for i in host_ip]
            # for i in host_ip:host_ip_list.append(i['h_ip'])

            # servicehealth = ServiceHealth(s_name,host_ip_list)
            # servicehealth.status_init()
            get_server_status.delay(iplist=host_ip_list,servername=s_name)

        else:
            server_status['sts'] = False
            server_status['rcode'] = 201
            server_status['msg'] = server_add_obj.errors.as_json()

        return JsonResponse(server_status)



@login_required
def server_operation(request,sid,type):
    '''服务编辑'''
    if request.method == "GET":
        if  type == '1':  #服务编辑
            Service_obj = models.Service.objects.filter(s_id=sid).first()

            Service_MF_I = Service_MF(instance=Service_obj)
            return render(request, 'service/server_edit.html', {'Service_MF_I': Service_MF_I, 'sid':sid})
        elif type == '2': #服务删除
            s_obj = models.Service.objects.filter(s_id=sid).values()

            models.Service_Status.objects.filter(server_name=s_obj[0]['s_name']).delete()

            models.Service.objects.filter(s_id=sid).delete()
            return HttpResponse(200)

    elif request.method == "POST":
        if type == '3':   #服务修改
            Service_obj = models.Service.objects.filter(s_id=sid).first()
            old_hid = []
            for i in Service_obj.h_server.all().values('id'):old_hid.append('{}'.format(i['id']))
            new_hid = request.POST.getlist('h_server')

            print (request.POST)

            Service_MF_I = Service_MF(request.POST,instance=Service_obj)
            if Service_MF_I.is_valid():
                Service_MF_I.save()

                del_host = [i for i in old_hid if i not in new_hid]

                if del_host:
                    print (del_host)
                    host_ip = Asset.objects.filter(id__in=del_host).values('manage_ip')

                    host_ip_list = []

                    for i in host_ip:host_ip_list.append(i['manage_ip'])

                    models.Service_Status.objects.filter(server_name=request.POST.get('s_name'),server_host__in=host_ip_list).delete()

                add_host = [i for i in new_hid if i not in old_hid]
                if add_host:
                    print ('add:',add_host)
                    host_ip = Asset.objects.filter(id__in=add_host).values('manage_ip')
                    host_ip_list = []
                    print ('hostlist:',host_ip_list)
                    for i in host_ip: host_ip_list.append(i['manage_ip'])
                    print ('name:',request.POST.get('s_name'))
                    print('hostlist:', host_ip_list)
                    # servicehealth = ServiceHealth(request.POST.get('s_name'), host_ip_list)
                    # servicehealth.status_init()
                    get_server_status.delay(iplist=host_ip_list, servername=request.POST.get('s_name'))

                return HttpResponse(200)
            else:
                return HttpResponse('你想搞什么')

@login_required
def server_control_list(request,s_name,s_type):
    '''控制Linux主机中的应用服务'''

    if request.method == "GET":


        server_m_host_obj = models.Service.objects.filter(s_name=s_name).first()
        # server_host_ip = models.Service_Status.objects.filter(server_name=s_name).values('server_host')
        # server_host_ip_list = []
        # for i in server_host_ip:
        #     server_host_ip_list.append(i['server_host'])
        # servicehealth = ServiceHealth(s_name, server_host_ip_list)
        # servicehealth.status_get()
        server_status_obj = models.Service_Status.objects.filter(server_name=s_name)

        return render(request, 'service/server_control.html', {"server_m_host_obj": server_m_host_obj,
                                                      "server_name": s_name,
                                                      "server_type":s_type,
                                                      'server_status_obj':server_status_obj})

@login_required
def server_control_action(request):

    '''启停服务'''
    if request.method == "POST":
        ip = request.POST.get('ip',None)
        server = request.POST.get('server',None)
        action = request.POST.get('action',None)
        server_type = request.POST.get('server_type',None)
        print (ip,server,action)
        bat_action = request.POST.get('bat_cli',None)

        callback = {}

        if bat_action:
            pass
        else:
            from tasks.tasks import control_host_server
            rr = APBase.getRedisConnection()
            try:

                r = control_host_server.delay(ip, action, server)
                rr.set('ServerCenter-{}-{}'.format(ip, server), r.id, ex=300)
            except Exception as  e:

                callback['result'] = 500
                callback['msg'] = str(e)
                return JsonResponse(callback)


            callback['result'] = 200
            return JsonResponse(callback)
            # rbt = ANSRunner([])
            # rbt.run_model(host_list=[ip],
            #               module_name='script',
            #               module_args='/opt/DOM/server.sh {} {}'.format(action,server)
            #
            #               )
            # data = rbt.get_model_result()
            # if data['success']:
            #     for k,v in data['success'].items():
            #         print (k,v['stdout_lines'][-1])
            #         status = v['stdout_lines'][-1]
            #         status_obj = json.loads(status)
            #         print (status_obj['meters']['status'])
            #         if status_obj['meters']['status'] == 1:
            #             callback['result'] = 200
            #         else:
            #             callback['result'] = 404
            # else:
            #     callback['result'] = 405
            # return JsonResponse(callback)


        # print (bat_action_list)
        # from utils._paramiko_example import  SSH_CLIENT
        # a_client = SSH_CLIENT('192.168.79.133', 22, 'root', 'redhat')
        # a_client.tactics()
        # a_client.conn()
        # if server_type == 'os':
        #
        #     cli_res = a_client.output("ansible {}  -m service -a 'name={} state={}'".format(ip,server,action))
        #
        #     # models.LogServer.objects.create(log_type="server",module='null',description="1111111",status="succeed")
        #     # 在这里执行重启的linux的相关服务
        #     # 判断返回值是否重启成功并写日志
        #     # result = serializers.serialize("json",models.LogServer.objects.filter(log_type="server",run_status="succeed"))
        #     # print (result)
        #     callback['status'] = "succeed"
        #     callback['result'] = cli_res
        #     return HttpResponse(json.dumps(callback))
        #
        # elif server_type == 'app':
        #     # test = "ansible {}  -m shell -a '/usr/local/ops/ops_test.sh {} {}'".format(ip, server, action)
        #     cli_res = a_client.output("ansible {}  -m shell -a '/usr/local/ops/ops_test.sh {} {}'".format(ip, server, action))
        #     callback['status'] = "succeed"
        #     callback['result'] = cli_res
        #
        #     return HttpResponse(json.dumps(callback))
        # elif bat_action != None:
        #     bat_action_list = json.loads(bat_action)
        #     callback_list = []
        #     for i in bat_action_list:
        #         a_client = SSH_CLIENT('192.168.79.133', 22, 'root', 'redhat')
        #         a_client.tactics()
        #         a_client.conn()
        #         if i["t"] == 'os':
        #             cli_res = a_client.output("ansible {}  -m service -a 'name={} state={}'".format(i['h'], i['s'], i['a']))
        #             callback['status'] = "succeed"
        #             callback['result'] = cli_res
        #         elif i["t"] == 'app':
        #             cli_res = a_client.output("ansible {}  -m shell -a '/usr/local/ops/ops_test.sh {} {}'".format(i['h'], i['s'], i['a']))
        #             callback['status'] = "succeed"
        #             callback['result'] = cli_res
        #             callback_list.append(callback)
        #
        #
        #     return JsonResponse({"bat_cli":callback_list})
@login_required
def server_control_action_result(request):
    '''启停服务log'''
    rr = APBase.getRedisConnection()
    ip = request.GET.get('ip')
    server = request.GET.get('server')

    rr_result_uuid = rr.get('ServerCenter-{}-{}'.format(ip,server))
    from celery.result import AsyncResult
    try:
        task_obj = AsyncResult(rr_result_uuid)
    except ValueError:
        return render(request, 'service/server_control_result.html', {'result': '未执行过命令'})


    if task_obj.ready():

        return render(request,'service/server_control_result.html',{'result':task_obj.result})
    else:
        return render(request, 'service/server_control_result.html', {'result': '任务执行中，请稍等！！（搞个刷新按钮）'})

