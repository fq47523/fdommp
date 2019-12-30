from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from .dao import DBManage
import json


#soar
from conf.soarconfig  import HOST
from conf.soarconfig import PORT
from conf.soarconfig import DEBUG
# from core.check import check_env
from databases.soar.common import soar_result
from databases.soar.common import soar_args_check
from databases.soar.common import open_brower



from databases.soar.argcrypto import decrypt





class DatabaseManage(LoginRequiredMixin,DBManage,View):


    def get(self, request, *args, **kwagrs):
        if request.GET.get('type'):
            res = self.allowcator(request.GET.get('type'), request)
            if isinstance(res, str): return JsonResponse({'msg': res, "code": 500, 'data': []})
            return JsonResponse({'msg': "查询成功", "code": 200, 'data': res})
        return render(request, 'database/db_manage.html', {"user": request.user})


    def post(self, request, *args, **kwagrs):
        res = self.allowcator(request.POST.get('model'), request)
        if isinstance(res, str): return JsonResponse({'msg': res, "code": 500, 'data': []})
        print (res)
        return JsonResponse({'msg': "操作成功", "code": 200, 'data': res})


class DatabaseQuery(LoginRequiredMixin, DBManage, View):
    login_url = '/login/'

    # @method_decorator_adaptor(permission_required, "Databases.databases_query_database_server_config", "/403/")
    def get(self, request, *args, **kwagrs):
        return render(request, 'database/db_query.html', {"user": request.user})

# SOAR
def SoarIndex(request):
    return render(request,'database/db_soar.html')

def SoarCmd(request):
    if request.method == 'POST':
        arg = json.loads(request.body.decode('utf-8'))

        if 'data' not in arg or 'key' not in arg:
            return JsonResponse({
                "result": 'data or key is None',
                "status": False
            })

        try:
            args = json.loads(decrypt(arg['data'], arg['key']))
        except Exception as e:
            return JsonResponse({
                "result": str(e),
                "status": False
            })

        if DEBUG:
            print(args)

        check = soar_args_check(args)
        if check:
            return HttpResponse(check,content_type='application/json')
        result = soar_result(args)

        return HttpResponse(result,content_type='application/json')


