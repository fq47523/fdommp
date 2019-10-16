from django.contrib import auth
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.views.generic import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator







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
            return HttpResponseRedirect('/')
        else:
            if request.method == "POST":

                return render(request, 'accounts/login.html', {"login_error_info": "用户名或者密码错误", "username":username}, )
            else:
                return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login')