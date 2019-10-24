from django.contrib import auth
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin

# from rest_framework_jwt.settings import api_settings
#
#
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER




class Index(LoginRequiredMixin,View):
    login_url = '/login/'


    def get(self, request, *args, **kwagrs):

        return render(request, 'accounts/index.html')



def login(request):
    if request.session.get('username') is not None:


        return HttpResponseRedirect('/')
    else:

        username = request.POST.get('user')
        password = request.POST.get('pwd')
        user = auth.authenticate(username=username,password=password)
        if user and user.is_active:

            auth.login(request,user)
            request.session['username'] = username

            request.session.set_expiry(3600)
            return HttpResponseRedirect('/')
            # payload = jwt_payload_handler(user)
            # token = jwt_encode_handler(payload)
            #
            # rep = HttpResponseRedirect('/')
            # rep.set_cookie('JwtToken',token,max_age=3598)
            # return rep
        else:
            if request.method == "POST":

                return render(request, 'accounts/login.html', {"login_error_info": "用户名或者密码错误", "username":username}, )
            else:
                return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')



class Permission(View):
    def get(self, request, *args, **kwagrs):
        return render(request, 'error/403.html', {"user": request.user})

    def put(self, request, *args, **kwagrs):
        return JsonResponse({'msg': "你没有权限操作此项", "code": 403, 'data': []})

    def post(self, request, *args, **kwagrs):
        return JsonResponse({'msg': "你没有权限操作此项", "code": 403, 'data': []})

    def delete(self, request, *args, **kwagrs):
        return JsonResponse({'msg': "你没有权限操作此项", "code": 403, 'data': []})