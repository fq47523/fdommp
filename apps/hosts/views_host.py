from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from assets.models import Asset
from utils._BT_pagination import BtPaging
import json
from django.views.decorators.csrf import csrf_exempt




# Create your views here.


@login_required
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



@login_required
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
