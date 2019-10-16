from django.http import JsonResponse
from hosts import models
from api.utils.zabbix_api_data import za_dashboard_data




# Create your views here.
def dashboard_data(request,type):
    '''dashboard数据源'''

    from django.db.models import Sum
    dashboard_za = za_dashboard_data()
    if request.method == "GET":

        if type == "host_off_line":
            host_off_line_obj = models.Host_zabbix.objects.filter(za_action=1).count()
            print (host_off_line_obj)
            return JsonResponse({'host_off_line':host_off_line_obj})

        elif type == 'server_off_line':
            server_off_line_obj = models.Service_Status.objects.filter(server_status=2).count()
            return JsonResponse({'server_off_line': server_off_line_obj})

        elif type == 'cpu':
            try:
                cpu_total = dashboard_za.total_cpu()
                cpu_use = models.Host_zabbix.objects.all().aggregate(t=Sum('za_cpu'))
                callback_res = round((cpu_use['t'] / cpu_total)*100)
            except Exception as e:
                print (e)
                return JsonResponse({'cpu':''})
            return JsonResponse({'cpu':callback_res})

        elif type == 'mem':
            try:
                mem_total = dashboard_za.total_mem()
                mem_total_res = round(mem_total / 1024 /1024 /1024,2)

                mem_use = models.Host_zabbix.objects.all().aggregate(t=Sum('za_mem'))

                callback_res = round((mem_use["t"] / mem_total_res) * 100)
            except Exception as e:
                print (e)
                return JsonResponse({'mem':''})

            return JsonResponse({"mem":callback_res})

        elif type == 'disk':
            try:
                disk_total = dashboard_za.total_disk()
                disk_use = models.Host_zabbix.objects.all().aggregate(t=Sum('za_disk'))

                callback_res = round((disk_use["t"] / disk_total) * 100)
            except Exception as e:
                print(e)
                return JsonResponse({'disk': ''})

            return JsonResponse({"disk": callback_res})

        elif type == 'net':
            try:
                net_in_total = dashboard_za.total_net(5,'net.if.in')
                net_out_total = dashboard_za.total_net(5,'net.if.out')
            except Exception as e:
                print(e)
                return JsonResponse({"net":{"net_in_total":'',"net_out_total":''}})
            # test = {"net":{"net_in_total":net_in_total,"net_out_total":net_out_total}}
            # print (test)
            return JsonResponse({"net":{"net_in_total":net_in_total,"net_out_total":net_out_total}})