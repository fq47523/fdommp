from django.views.generic import View
from django.http import JsonResponse
from django.shortcuts import render
from .dao import DBManage





class DatabaseManage(DBManage,View):


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