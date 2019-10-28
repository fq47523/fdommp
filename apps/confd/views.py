from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import django.utils.timezone as timezone
from confd.modelform.confd_modelform import Confd_MF
from hosts.models import Service

from utils._BT_pagination import BtPaging
from hosts.models import Confd,Confd_Update_History
from assets.models import  Asset
from api.utils.ansible_api import ANSRunner
import json,os,shutil



serverconf_dir = os.path.dirname(os.path.realpath(__file__)) + '/serverconf/'
status = {"sts": None, "msg": None}


# Create your views here.
@login_required
def confd_list(request):
    if request.method == 'GET':

        return render(request,'confd/confd.html')

    if request.method == 'POST':

        page_json = json.loads(request.body)

        confd_paging_date = BtPaging(Confd, page_json)
        confd_paging_date_ret = confd_paging_date.confd_paging()

        return JsonResponse(confd_paging_date_ret)

@login_required
def confd_add(request):
    if request.method == 'GET':
        Confd_MF_init = Confd_MF()

        return render(request,'confd/confd_add.html',locals())

    if request.method == 'POST':


        conf_name = request.POST['conf_name']
        conf_file_path = request.POST['conf_path']
        host_id = request.POST['conf_host']
        host_ip = [i['manage_ip'] for i in Asset.objects.filter(id=host_id).values('manage_ip')]

        # init_dir = serverconf_dir+host_ip[0]+'/{}/'.format(conf_name)
        init_dir = serverconf_dir+'{}/'.format(conf_name)+host_ip[0]+'/'


        if not os.path.isdir(init_dir):
            os.makedirs(init_dir)



        rbt = ANSRunner([], redisKey='1')
        rbt.run_model(host_list=host_ip, module_name='fetch',
                      module_args='src=\"{}\" dest=\"{}\" flat=\"yes\"'.format(conf_file_path,init_dir))
        data = rbt.get_model_result()

        if data['success']:

            Confd_MF_obj = Confd_MF(request.POST)
            if Confd_MF_obj.is_valid():
                Confd_MF_obj.save()
                status['sts'] = True
                status['rcode'] = 200
            else:
                status['sts'] = False
                status['rcode'] = 500
                status['msg'] = Confd_MF_obj.errors.as_json()


        elif data['failed']:
            os.rmdir(init_dir)
            status['sts'] = False
            status['rcode'] = 404
            status['msg'] = '文件名或路径错误'

        elif data['unreachable']:
            os.rmdir(init_dir)
            status['sts'] = False
            status['rcode'] = 502
            status['msg'] = '网络错误或请求不可达'


        return  JsonResponse(status)


@login_required
def confd_edit(request,confd_id):
    if request.method == 'GET':
        confd_id = confd_id
        confd_obj = Confd.objects.filter(id=confd_id).first()
        host_ip = confd_obj.conf_host.all().values('manage_ip')
        file_path = confd_obj.conf_path
        conf_name = confd_obj.conf_name

        edit_obj = serverconf_dir + '{}/{}/{}'.format(conf_name,host_ip[0]['manage_ip'],file_path.split('/')[-1])

        with open(edit_obj,'r') as f:
            file_obj = f.read()

        return render(request,'confd/confd_edit.html',locals())

    if request.method == 'POST':

        file_obj = request.POST.get('file',None)
        file_ip = request.POST.get('host_ip',None)
        file_path = request.POST.get('file_path',None)
        file_dir = request.POST.get('conf_name',None)

        edit_save_obj = serverconf_dir + '{}/{}/{}'.format(file_dir,file_ip,file_path.split('/')[-1])

        with open(edit_save_obj,'w') as f:
            f.write(file_obj)
            cc = Confd.objects.filter(id=confd_id).first()
            Confd.objects.filter(id=confd_id).update(edit_date=timezone.now(), modified_ver=cc.modified_ver + 1)
            status['sts'] = True
            status['rcode'] = 200
            status['msg'] = ''

        return JsonResponse(status)


@login_required
def confd_init(request):
    if request.method == 'POST':
        print (request.POST)
        confd_init_status = {}
        conf_id = request.POST.get('conf_id',None)
        host_ip = request.POST.get('host_ip',None)
        server_type = request.POST.get('server_type',None)
        conf_name = request.POST.get('conf_name',None)
        conf_path = request.POST.get('conf_path',None)

        get_conf_ver = Confd.objects.filter(conf_name=conf_name).first()
        init_filename = conf_path.split('/')[-1]+'.{}'.format(get_conf_ver.current_ver)
        backup_path = serverconf_dir + '{}/{}/{}'.format(conf_name,host_ip,init_filename)

        rbt = ANSRunner([], redisKey='1')
        rbt.run_model(host_list=[host_ip], module_name='fetch',
                      module_args='src=\"{}\" dest=\"{}\" flat=\"yes\"'.format(conf_path, backup_path))
        data = rbt.get_model_result()

        if data['success']:
            confd_init_status['backupfile'] = True
            src = serverconf_dir + '{}/{}/{}'.format(conf_name,host_ip,conf_path.split('/')[-1])
            dest = conf_path


            rbt = ANSRunner([], redisKey='1')
            rbt.run_model(host_list=[host_ip], module_name='copy',
                          module_args='src=\"{}\" dest=\"{}\"'.format(src, dest))
            data = rbt.get_model_result()
            # data_json = json.dumps(data, indent=4)

            if data['success']:
                confd_init_status['pushfile'] = True
                # import requests as req
                #
                # url = "http://192.168.79.134:8080/accounts/login/"
                # s = req.session()  # 建立一个Session
                # print (host_ip,server_type)
                # response = s.post(url, data={"user": "api", "pwd": "api"})  # session登录网站
                # response = s.post("http://192.168.79.134:8080/service/control_action/",
                #                   data={"ip": host_ip, "server": server_type, "action": "restarted"})  # session浏览页面
                # response.encoding = "utf-8"
                # response_ret = response.json()
                # s.get("http://192.168.79.134:8080/accounts/login/")
                rbt = ANSRunner([], redisKey='1')
                # Ansible Adhoc
                rbt.run_model(host_list=[host_ip], module_name='script',
                              module_args='/opt/DOM/server.sh {} {}'.format("restarted", server_type))

                data = rbt.get_model_result()


                if data['success']:
                    Confd.objects.filter(conf_name=conf_name).update(current_ver=get_conf_ver.modified_ver)
                    Confd_Update_History.objects.create(conf_id=conf_id,
                                                        conf_ip=host_ip,
                                                        conf_name=conf_name,
                                                        conf_server=server_type,
                                                        backup_ver=get_conf_ver.current_ver,
                                                        backup_path=backup_path,
                                                        target_path=conf_path
                                                        )
                    confd_init_status['server_restart'] = True
                    confd_init_status['rcode'] = 200
                    print (confd_init_status)
                else:
                    confd_init_status['server_restart'] = False
                    confd_init_status['rcode'] = 500
                    confd_init_status['msg'] = '服务重启失败'
            else:
                confd_init_status['pushfile'] = False
                confd_init_status['rcode'] = 500
                confd_init_status['msg'] = '网络或路径错误'

        else:
            confd_init_status['backupfile'] = False
            confd_init_status['rcode'] = 500
            confd_init_status['msg'] = '网络或路径错误'

        return HttpResponse(200)

@login_required
def confd_rollback(request):
    if request.method == 'GET':
        print(request.GET)
        conf_id = request.GET.get('conf_id',None)

        return render(request,'confd/confd_rollback.html',locals())

    if request.method == 'POST':
        rollback_on = request.POST.get('rollback', None)

        if rollback_on:
            confd_rollback_status = {}

            conf_id = request.POST['conf_id']
            backup_ver = request.POST['backup_ver']

            print (request.POST['conf_id'])
            rollback_obj = Confd_Update_History.objects.filter(conf_id=conf_id,backup_ver=backup_ver).first()

            rbt = ANSRunner([], redisKey='1')
            rbt.run_model(host_list=[rollback_obj.conf_ip], module_name='copy',
                          module_args='src=\"{}\" dest=\"{}\"'.format(rollback_obj.backup_path, rollback_obj.target_path))
            data = rbt.get_model_result()
            # data_json = json.dumps(data, indent=4)

            if data['success']:
                confd_rollback_status['pushfile'] = True

                rbt = ANSRunner([], redisKey='1')
                # Ansible Adhoc
                rbt.run_model(host_list=[rollback_obj.conf_ip], module_name='script',
                              module_args='/opt/DOM/server.sh {} {}'.format("restarted", rollback_obj.conf_server))

                data = rbt.get_model_result()

                if data['success']:
                # if
                    Confd.objects.filter(id=rollback_obj.conf_id).update(current_ver=backup_ver)


            return HttpResponse(200)


        page_json = json.loads(request.body)
        if page_json:
            confd_rollback_data = BtPaging(Confd_Update_History, page_json)
            confd_rollback_data_ret = confd_rollback_data.confd_rollback_paging(page_json['conf_id'])
            return JsonResponse(confd_rollback_data_ret)





@login_required
def confd_del(request):
    if request.method == "POST":

        conf_id = request.POST.get('conf_id',None)
        conf_name = request.POST.get('conf_name',None)

        Confd.objects.filter(id=conf_id).delete()
        Confd_Update_History.objects.filter(conf_name=conf_name).delete()
        delete_obj = serverconf_dir + '{}/'.format(conf_name)
        shutil.rmtree(delete_obj)
        status['sts'] = 200
        status['msg'] = 'delete succeed'
        return JsonResponse(status)