from django.conf import settings
from fdommp.celery import app
from celery import  shared_task
from celery.schedules import crontab
from api.utils.ansible_api import ANSRunner
from hosts import models
from assets.models import Asset
from api.utils.zabbix_api import Zabbix_API
from utils._paramiko_example import SSH_CLIENT
import time,json
from datetime import timedelta


'''
 启动:venv/bin/celery  -A fdommp  worker -B -l info
	venv/bin/celery ：pip 虚拟环境下的bin脚本
	-A ：启动那个应用
	fdommp ：app(在django中settings上层目录)
	worker ：启动类型（进程）
	-B ：启动定时任务
	-l ：控制台输出日志级别
	celery multi start w1 -A fdommp  -l info --logfile=/home/fuqing/PycharmProjects/fdommp/logs/celery.log
	celery multi stop w1
'''

app.conf.beat_schedule = {

'get_hosts_status': {

'task': 'tasks.tasks.get_hosts_status',

'schedule': timedelta(seconds=300),

'args': ()

},
'get_server_status': {

'task': 'tasks.tasks.get_server_status',

'schedule': timedelta(seconds=300),

'args': ()

},

# 'crontab_test':{
# 'task': 'tasks.tasks.add',
# 'schedule': crontab(hour='15', minute='10', day_of_week='*'),
# 'args': (7,7)
# }

}

# test
@app.task
def add(x, y):

    return x + y

# test
@shared_task
def control_host_server(ip,action,server):
    rbt = ANSRunner([], redisKey='1')
    # Ansible Adhoc
    rbt.run_model(host_list=[ip], module_name='script', module_args='{} {} {}'.format(settings.SERVER_SHELL_SCRIPT,action,server))
    data = rbt.get_model_result()
    if data['success']:
        for k, v in data['success'].items():

             status = v['stdout_lines'][-1]
             status_obj = json.loads(status)

             if status_obj['meters']['status'] == 1:
                 models.Service_Status.objects.filter(server_host=ip,server_name=server).update(server_status=1)
             elif status_obj['meters']['status'] == 11:
                 models.Service_Status.objects.filter(server_host=ip, server_name=server).update(server_status=2)
             elif status_obj['meters']['status'] == 2:
                 models.Service_Status.objects.filter(server_host=ip, server_name=server).update(server_status=5)


    if data['failed']:
        models.Service_Status.objects.filter(server_host=ip, server_name=server).update(server_status=3)
    if data['unreachable']:
        models.Service_Status.objects.filter(server_host=ip, server_name=server).update(server_status=4)
    return data



@app.task(ignore_result=True)
def get_hosts_status():
    '''
    获取zabbix客户端中主机的存活，cpu，men，disk使用量,并写入数据库
    :return:
    '''
    zabbix_init = Zabbix_API()
    hostid_list = zabbix_init.host_get()


    for host_dict in hostid_list:
        host_obj = Asset.objects.filter(manage_ip=host_dict['interfaces'][0]['ip']).first()
        if not host_obj: continue

        za_action = zabbix_init.za_agent_action(host_dict['hostid'])
        za_cpu_system = zabbix_init.za_agent_cpu_system(host_dict['hostid'])
        za_cpu_user = zabbix_init.za_agent_cpu_user(host_dict['hostid'])
        za_mem_available = zabbix_init.za_agent_mem(host_dict['hostid'])
        za_mem_total = zabbix_init.host_mem_total(host_dict['hostid'])
        za_disk = zabbix_init.za_agent_disk(host_dict['hostid'])

        host_dict['za_action'] = int(za_action[0]['value'])
        host_dict['za_cpu'] = round(float(za_cpu_system[0]['lastvalue']) + float(za_cpu_user[0]['lastvalue']), 2)
        host_dict['za_mem'] = round(
            (int(za_mem_total[0]['lastvalue']) - int(za_mem_available[0]['lastvalue'])) / 1024 / 1024 / 1024, 2)
        host_dict['za_disk'] = round(int(za_disk[0]['lastvalue']) / 1024 / 1024 / 1024, 2)

        obj, create = models.Host_zabbix.objects.update_or_create(
            za_ip=host_dict['interfaces'][0]['ip'],
            defaults={
                'za_action': host_dict.get('za_action'),
                'za_cpu': host_dict.get('za_cpu', 0),
                'za_mem': host_dict.get('za_mem', 0),
                'za_disk': host_dict.get('za_disk', 0),
                'asset_extend': host_obj,
            }

        )

@app.task(ignore_result=True)
def get_server_status(iplist=None,servername=None):
    '''获取服务状态'''
    if iplist and servername:
        # 初始化时创建服务状态
        serverlist_dict = {servername:iplist}
        for server_k in serverlist_dict:
            rbt = ANSRunner([])
            rbt.run_model(host_list=serverlist_dict[server_k], module_name='shell',
                          module_args='ps -ef  | grep -w {} | grep -v grep | wc -l'.format(server_k))
            data = rbt.get_model_result()

            if data['success']:
                for k, v in data['success'].items():
                    ip = str(k)
                    stdout_code = int(v['stdout'])

                    if stdout_code > 0:
                        models.Service_Status.objects.create(server_name=server_k,server_host=ip.replace('_', '.'),server_status=1)
                    elif stdout_code == 0:
                        models.Service_Status.objects.create(server_name=server_k,server_host=ip.replace('_', '.'),server_status=2)
            if data['failed']:
                for k, v in data['failed'].items():
                    ip = str(k)
                    models.Service_Status.objects.create(server_name=server_k,server_host=ip.replace('_', '.'),server_status=3)
            if data['unreachable']:
                for k, v in data['unreachable'].items():
                    ip = str(k)
                    models.Service_Status.objects.create(server_name=server_k,server_host=ip.replace('_', '.'),server_status=4)

    else:
        # 轮询时更新服务状态
        serverlist_dict = {}

        for server_obj in models.Service.objects.all():
            serverlist_dict[server_obj.s_name] = [ii['h_ip'] for ii in server_obj.h_server.all().values('h_ip')]

        for server_k in serverlist_dict:
            rbt = ANSRunner([])
            rbt.run_model(host_list=serverlist_dict[server_k], module_name='shell', module_args='ps -ef  | grep -w {} | grep -v grep | wc -l'.format(server_k))
            data = rbt.get_model_result()

            if data['success']:
                for k,v in data['success'].items():
                    ip = str(k)
                    stdout_code = int(v['stdout'])

                    if stdout_code > 0:
                        models.Service_Status.objects.filter(server_name=server_k,server_host=ip.replace('_','.'),).update(server_status=1)
                    elif stdout_code == 0:
                        models.Service_Status.objects.filter(server_name=server_k,server_host=ip.replace('_', '.'),).update(server_status=2)

            if data['failed']:
                for k,v in data['failed'].items():
                    ip = str(k)
                    models.Service_Status.objects.filter(server_name=server_k,server_host=ip.replace('_', '.'),).update(server_status=3)

            if data['unreachable']:
                for k,v in data['unreachable'].items():
                    ip = str(k)
                    models.Service_Status.objects.filter(server_name=server_k,server_host=ip.replace('_', '.'),).update(server_status=4)