from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from hosts import models
from assets.models import Asset
from api.utils.ansible_api import *
from utils._auth import session_auth
from utils._get_files import get_scripts,get_roles
from hosts.modelform.crontab_modelform import Crontab_MF,Crontab_Edit_MF,Crontab_Add_Host_MF
from django.core import serializers
import json,os


pwd = os.path.dirname(os.path.realpath(__file__))
script = pwd + "/script/sh/"
playbook = pwd + "/script/playbook/"
playbook_roles = pwd + "/script/roles/"


def automate_shell(request):
    if request.method == 'GET':
        script_list = get_scripts(script)
        hosts = models.Host_zabbix.objects.filter(za_action=0).values('za_ip')

        return render(request, 'hosts/automate_shell.html', locals())
    elif request.method == 'POST':
        ansible_host = request.POST.getlist('mserver',None)
        ansible_script = request.POST.get('mscripts',None)
        ansible_command = request.POST.get('mcommand',None)
        if ansible_host and ansible_command:
            rbt = ANSRunner([])
            rbt.run_model(host_list=ansible_host, module_name='shell', module_args=ansible_command)
            data = rbt.get_model_result()
            # print (request.POST)
            print (json.dumps(data,indent=4))
            with open('logs/ansible_execshell.log','w+',encoding='UTF-8') as f:
                json.dump(data,f,ensure_ascii=False)

            return HttpResponse('200')

        if ansible_host and ansible_script:
            rbt = ANSRunner([])
            rbt.run_model(host_list=ansible_host, module_name='script', module_args=script+ansible_script)
            data = rbt.get_model_result()
            # print (request.POST)
            print(json.dumps(data, indent=4))
            with open('logs/ansible_execshell.log', 'w+', encoding='UTF-8') as f:
                json.dump(data, f, ensure_ascii=False)


            return HttpResponse('200')


def automate_playbook(request):
    if request.method == 'GET':
        playbook_list = get_scripts(playbook)
        playbook_roles_list = get_roles(playbook_roles)
        hosts = models.Host_zabbix.objects.filter(za_action=0).values('za_ip')
        return render(request, 'hosts/automate_playbook.html', locals())

    if request.method == 'POST':

        ansible_host = request.POST.getlist('mserver',None)
        ansible_playbook = request.POST.get('splaybook',None)
        ansible_playbook_roles = request.POST.get('mroles',None)

        if ansible_host and ansible_playbook:
            rbt = ANSRunner([])
            rbt.run_playbook(playbook_path=playbook+ansible_playbook,
                             extra_vars={"h":ansible_host})
            data = rbt.get_playbook_result()
            with open('logs/ansible_playbook.log', 'w+', encoding='UTF-8') as f:
                json.dump(data, f, ensure_ascii=False)


            return  HttpResponse(200)

        if ansible_host and ansible_playbook_roles:
            print (ansible_host,ansible_playbook_roles)
            rbt = ANSRunner([])
            rbt.run_playbook(playbook_path=playbook_roles + 'main.yml',
                             extra_vars={"hh": ansible_host,'rr':ansible_playbook_roles})
            data = rbt.get_playbook_result()
            with open('logs/ansible_playbook.log', 'w+', encoding='UTF-8') as f:
                json.dump(data, f, ensure_ascii=False)



            return HttpResponse(200)






def automate_shell_result(request,ansible_type):
    if request.method == 'GET':
        print (ansible_type)
        if ansible_type == 'shell':
            with open('logs/ansible_execshell.log','r',encoding='UTF-8') as f:
                data = json.load(f)

            # print (data)

            return render(request, 'hosts/automate_shell_result.html', {'result':data})


def automate_playbook_result(request,ansible_type):
    if request.method == 'GET':
        print (ansible_type)
        if ansible_type == 'playbook':
            with open('logs/ansible_playbook.log','r',encoding='UTF-8') as f:
                data = json.load(f)

            # print (data)

            return render(request, 'hosts/automate_playbook_result.html', {'result':data})







def automate_crontab(request):
    crontab_obj = models.Crontab.objects.all()
    return render(request, 'hosts/automate_crontab.html', {'crontab_obj':crontab_obj})

def automate_crontab_add(request):


    if request.method == 'POST':

        crontab_jobname = request.POST.get('jobname')
        # crontab_minute = request.POST.get('minute')
        # crontab_hour = request.POST.get('hour')
        # crontab_day = request.POST.get('day')
        # crontab_month = request.POST.get('month')
        # crontab_weekday = request.POST.get('weekday')
        # crontab_jobcli = request.POST.get('jobcli')
        crontab_host = request.POST.getlist('cron_host')

        Crontab_MF_obj = Crontab_MF(request.POST)
        if Crontab_MF_obj.is_valid():
            Crontab_MF_obj.save()



            ansible_host_list = []
            host_list = Asset.objects.filter(id__in=crontab_host).values('manage_ip')


            for i in host_list:
                ansible_host_list.append(i['manage_ip'])

            for host in ansible_host_list:
                models.Crontab_Status.objects.create(job_name=crontab_jobname, job_host=host, job_status=99)

            return JsonResponse({'status':200})
        else:
            return JsonResponse({'status': 500})

    if request.method == 'GET':
        crontab_modelform = Crontab_MF()

        return render(request, 'hosts/automate_crontab_add.html', {'crontab_modelform':crontab_modelform})


def automate_crontab_add_host(request,job_name):
    if request.method == 'GET':
        crontab_obj = models.Crontab.objects.filter(jobname=job_name).first()
        Crontab_Add_Host = Crontab_Add_Host_MF(instance=crontab_obj)
        return render(request, 'hosts/automate_crontab_add_host.html', {'Crontab_Add_Host':Crontab_Add_Host, 'job_name':job_name})

    if request.method == 'POST':
        hosts_id = request.POST.getlist('cron_host',None)
        crontab_obj = models.Crontab.objects.filter(jobname=job_name).first()
        hosts_obj = Asset.objects.filter(id__in=hosts_id)
        crontab_obj.cron_host.add(*hosts_obj)
        for host in hosts_obj.values():
            models.Crontab_Status.objects.create(job_name=job_name, job_host=host['manage_ip'], job_status=99)

        return HttpResponse(200)


def automate_crontab_edit(request,job_name):
    if request.method == 'POST':
        print (request.POST)
        crontab_obj = models.Crontab.objects.filter(jobname=job_name).first()
        Crontab_MF_Edit = Crontab_Edit_MF(request.POST,instance=crontab_obj)
        if Crontab_MF_Edit.is_valid():
            Crontab_MF_Edit.save()

            crontab_obj_new = models.Crontab.objects.filter(jobname=job_name)
            cron_json = serializers.serialize('json', crontab_obj_new)
            cron_dict = json.loads(cron_json)
            cron_res = cron_dict[0]['fields']

            ansible_host_list = []
            cron_obj_sts = models.Crontab_Status.objects.all()
            for cron_obj in crontab_obj_new:
                for host_ip in cron_obj.cron_host.all():
                    print (host_ip)
                    ansible_host_list.append(str(host_ip))


                    for cron_obj_sts_obj in cron_obj_sts:
                        # print(host_ip,cron_obj_sts_obj.job_host,cron_obj_sts_obj.job_name,cron_obj_sts_obj.job_status,cron_res['jobname'])
                        if str(host_ip) in cron_obj_sts_obj.job_host and cron_obj_sts_obj.job_name == cron_res['jobname'] and cron_obj_sts_obj.job_status == 1:
                            rbt = ANSRunner([])
                            rbt.run_model(host_list=ansible_host_list,
                                          module_name='cron',
                                          module_args='name=\"{}\" minute=\"{}\" hour=\"{}\" day=\"{}\" month=\"{}\" weekday=\"{}\" job=\"{}\"'.format(
                                              cron_res['jobname'],
                                              cron_res['minute'],
                                              cron_res['hour'],
                                              cron_res['day'],
                                              cron_res['month'],
                                              cron_res['weekday'],
                                              cron_res['jobcli'],
                                          )
                                          )
                            data = rbt.get_model_result()
                            print('11111:',data)
                            for k, v in data.items():
                                for kk, vv in v.items():
                                    if vv['changed']:
                                        pass

                        elif str(host_ip) in cron_obj_sts_obj.job_host and cron_obj_sts_obj.job_name == cron_res['jobname'] and cron_obj_sts_obj.job_status == 2:
                            rbt = ANSRunner([])
                            rbt.run_model(host_list=ansible_host_list,
                                          module_name='cron',
                                          module_args='name=\"{}\" minute=\"{}\" hour=\"{}\" day=\"{}\" month=\"{}\" weekday=\"{}\" job=\"{}\" disabled=\"yes\"'.format(
                                              cron_res['jobname'],
                                              cron_res['minute'],
                                              cron_res['hour'],
                                              cron_res['day'],
                                              cron_res['month'],
                                              cron_res['weekday'],
                                              cron_res['jobcli'],
                                          )
                                          )
                            data = rbt.get_model_result()
                            print('22222222:',data)
                            for k, v in data.items():
                                for kk, vv in v.items():
                                    if vv['changed']:
                                        pass
                        else:
                            pass

            return JsonResponse({'status':200})

    if request.method == 'GET':
        crontab_obj = models.Crontab.objects.filter(jobname=job_name).first()
        Crontab_MF_Edit = Crontab_Edit_MF(instance=crontab_obj)
        return render(request, 'hosts/automate_crontab_edit_task.html', {'Crontab_MF_Edit':Crontab_MF_Edit, 'job_name':job_name})




def automate_crontab_del(request):
    if request.method == 'POST':
        cron_jobname = request.POST.get('crontab_jobname',None)
        cron_hosts = request.POST.getlist('crontab_hosts[]',None)

        if cron_jobname  and cron_hosts:
            asset_sn = [i.split()[2] for i in cron_hosts]
            asset_iplist = [i.manage_ip for i in Asset.objects.filter(sn__in=asset_sn)]
            rbt = ANSRunner([])
            rbt.run_model(host_list=asset_iplist,
                          module_name='cron',
                          module_args='name=\"{}\" state=\"absent\"'.format(
                              cron_jobname,

                          )
                          )
            #data = rbt.get_model_result()
            # yuliu

        models.Crontab.objects.filter(jobname=cron_jobname).delete()
        models.Crontab_Status.objects.filter(job_name=cron_jobname).delete()
        return HttpResponse(200)







def automate_crontab_host(request,h_id):
    asset_obj = Asset.objects.filter(id=h_id)
    crontab_status_obj = models.Crontab_Status.objects.all()
    return render(request, 'hosts/automate_crontab_host.html', {'asset_obj':asset_obj, 'crontab_status_obj':crontab_status_obj})



def automate_crontab_host_action(request):
    if request.method == 'POST':
        print (request.POST)
        host_ip = request.POST.get('ip', None)
        cron_job_name = request.POST.get('job_name', None)
        cron_action_type = request.POST.get('type', None)

        cron_job = models.Crontab.objects.filter(jobname=cron_job_name)
        cron_json = serializers.serialize('json', cron_job)
        cron_dict = json.loads(cron_json)
        cron_res = cron_dict[0]['fields']

        if cron_action_type == 'cron_init':
            print (cron_res)
            rbt = ANSRunner([])
            rbt.run_model(host_list=['{}'.format(host_ip)],
                          module_name='cron',
                          module_args='name=\"{}\" minute=\"{}\" hour=\"{}\" day=\"{}\" month=\"{}\" weekday=\"{}\" job=\"{}\"'.format(
                                cron_res['jobname'],
                                cron_res['minute'],
                                cron_res['hour'],
                                cron_res['day'],
                                cron_res['month'],
                                cron_res['weekday'],
                                cron_res['jobcli'],
                                )
                          )
            data = rbt.get_model_result()
            print (data)
            for k, v in data.items():
                for kk, vv in v.items():
                    host_ip = str(kk)
                    if vv['changed']:
                        models.Crontab_Status.objects.filter(job_name=cron_job_name, job_host=host_ip.replace('_', '.')).update(job_status=1)
                        return HttpResponse(200)

        if cron_action_type == 'cron_pause':
            print (cron_res)
            rbt = ANSRunner([])
            rbt.run_model(host_list=['{}'.format(host_ip)],
                          module_name='cron',
                          module_args='name=\"{}\" minute=\"{}\" hour=\"{}\" day=\"{}\" month=\"{}\" weekday=\"{}\" job=\"{}\" disabled=\"yes\"'.format(
                                cron_res['jobname'],
                                cron_res['minute'],
                                cron_res['hour'],
                                cron_res['day'],
                                cron_res['month'],
                                cron_res['weekday'],
                                cron_res['jobcli'],
                                )
                          )
            data = rbt.get_model_result()
            print (data)
            for k, v in data.items():
                for kk, vv in v.items():
                    host_ip = str(kk)
                    if vv['changed']:
                        models.Crontab_Status.objects.filter(job_name=cron_job_name, job_host=host_ip.replace('_', '.')).update(job_status=2)
                        return HttpResponse(200)


        if cron_action_type == 'cron_continue':
            print (cron_res)
            rbt = ANSRunner([])
            rbt.run_model(host_list=['{}'.format(host_ip)],
                          module_name='cron',
                          module_args='name=\"{}\" minute=\"{}\" hour=\"{}\" day=\"{}\" month=\"{}\" weekday=\"{}\" job=\"{}\" disabled=\"no\"'.format(
                                cron_res['jobname'],
                                cron_res['minute'],
                                cron_res['hour'],
                                cron_res['day'],
                                cron_res['month'],
                                cron_res['weekday'],
                                cron_res['jobcli'],
                                )
                          )
            data = rbt.get_model_result()
            print (data)
            for k, v in data.items():
                for kk, vv in v.items():
                    host_ip = str(kk)
                    if vv['changed']:
                        models.Crontab_Status.objects.filter(job_name=cron_job_name, job_host=host_ip.replace('_', '.')).update(job_status=1)
                        return HttpResponse(200)




        if cron_action_type == 'cron_delete':
            print (cron_res)
            rbt = ANSRunner([])
            rbt.run_model(host_list=['{}'.format(host_ip)],
                          module_name='cron',
                          module_args='name=\"{}\" minute=\"{}\" hour=\"{}\" day=\"{}\" month=\"{}\" weekday=\"{}\" job=\"{}\" state=\"absent\"'.format(
                                cron_res['jobname'],
                                cron_res['minute'],
                                cron_res['hour'],
                                cron_res['day'],
                                cron_res['month'],
                                cron_res['weekday'],
                                cron_res['jobcli'],
                                )
                          )
            data = rbt.get_model_result()
            print (data)
            for k, v in data.items():
                for kk, vv in v.items():
                    host_ip = str(kk)
                    if vv['changed']:

                        models.Crontab_Status.objects.filter(job_name=cron_job_name, job_host=host_ip.replace('_', '.')).delete()
                        host_obj = Asset.objects.get(manage_ip=host_ip.replace('_', '.'))
                        cron_obj = models.Crontab.objects.filter(jobname=cron_job_name)
                        host_obj.crontab_set.remove(*cron_obj)
                        host_cron_count = host_obj.crontab_set.count()

                        return  JsonResponse({'status':200,'host_cron_count':host_cron_count})

