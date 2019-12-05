from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from .dao import DBManage





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