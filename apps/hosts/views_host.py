from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from hosts import models
from hosts.models import Host
from assets.models import Asset
from hosts.modelform.host_modelform import Host_MF
from utils._BT_pagination import BtPaging
from utils._auth import session_auth
import json





# Create your views here.



def host(request):
    # 返回主机列表，分页数据及标签

    if request.method == "GET":
        return render(request, 'hosts/host.html')
    if request.method == "POST":

        page_json = json.loads(request.body)
        # page_json = {'rows':int(request.POST['rows']),'page':int(request.POST['page']),'sortOrder':request.POST['sortOrder']}

        host_paginf_date = BtPaging(Asset, page_json)
        host_paginf_date_ret = host_paginf_date.host_paging()


        return JsonResponse(host_paginf_date_ret)



def host_add(request):
    if request.method == "GET":
        host_modelform = Host_MF()
        return render(request,'hosts/host_add.html',locals())


    if request.method == "POST":
        # 新建主机
        add_host_status = {"sts": None, "msg": None}
        host_add_obj = Host_MF(request.POST)
        if host_add_obj.is_valid():
            host_add_obj.save()
            add_host_status['sts'] = True
            add_host_status['rcode'] = 200
        else:
            add_host_status['sts'] = False
            add_host_status['rcode'] = 201
            add_host_status['msg'] = host_add_obj.errors.as_json()

        return JsonResponse(add_host_status)



def host_edit(request,h_id):
    if request.method == "GET":

        host_modelform = Host_MF(instance=models.Host.objects.filter(h_id=h_id).first())
        host_id = h_id
        return render(request,'hosts/host_edit.html',locals())

    if request.method == "POST":

        # add_host_status = {"sts": None, "msg": None}
        # # 编辑主机
        # edit_id = request.POST.get('edit_id',None)
        # if  edit_id:
        host_obj = models.Host.objects.filter(h_id=h_id).first()
        host_edit_obj = Host_MF(request.POST,instance=host_obj)
        if host_edit_obj.is_valid():
            host_edit_obj.save()




            return HttpResponse(200)


def host_del(request):
    '''删除主机'''
    hip = request.GET.get('hip',None)
    if hip:
        models.Host.objects.filter(h_ip=hip).delete()

        return HttpResponse(json.dumps({"status":"succeed"}))
    else:
        pass


def hostgroup(request):
    import redis

    pool = redis.ConnectionPool(decode_responses=True)
    rr = redis.Redis(connection_pool=pool)

    if request.method == "GET":
        celery_init = request.GET.get('celery_test')

        if celery_init:
            from tasks.tasks import ansi

            r = ansi.delay('192.168.79.134')

            rr.set('server-192.168.79.134-nginx', r.id, ex=60)



            cc = r.id

            return JsonResponse({'celery_id': cc})
        return render(request, 'hosts/hostgroup.html')


    if request.method == "POST":
        celery_id = request.POST.get('celery_id')

        # print (rr.get('server-192.168.79.134-nginx'),type(rr.get('server-192.168.79.134-nginx')))
        rr_result = rr.get('server-192.168.79.134-nginx')
        from celery.result import AsyncResult
        # uuid = str(rr_result)
        task_obj = AsyncResult(rr_result)
        if task_obj.ready():
            #print (task_obj.result)

            return JsonResponse({'result':task_obj.result})
