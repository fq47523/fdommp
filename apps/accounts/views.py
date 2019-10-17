from django.shortcuts import render,redirect
from accounts import models
from utils._auth import session_auth
from django.contrib.auth.decorators import login_required





# Create your views here.


# def login(request):
#     '''登入验证'''
#     error_msg = ""
#     if request.method == "POST":
#         user = request.POST.get("user",None)
#         pwd = request.POST.get("pwd",None)
#         user_passwd_ret = models.User.objects.filter(u_name=user).first()
#         if user_passwd_ret == None:
#             error_msg = "账户名或密码错误，请重新输入"
#         elif user_passwd_ret.u_pwd == pwd:
#             request.session['username'] = user
#             request.session['is_login'] = True
#             request.session.set_expiry(3600)
#             return redirect("/accounts/index/")
#         else:
#             error_msg = "账户名或密码错误，请重新输入"
#
#     return render(request, "accounts/login.html", {"error_msg":error_msg})
#
#
# def index(request):
#     return render(request, "accounts/index.html")
#
#
#
#
#
# def logout(request):
#     '''用户注销'''
#     # del request.session['username']
#     request.session.clear()
#     return redirect('/accounts/login/')

@login_required
def dashboard(request):
    '''dashboard首页'''
    return render(request, 'accounts/dashboard.html')

