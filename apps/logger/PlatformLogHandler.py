from django.utils.deprecation import MiddlewareMixin
from logger import models
from hosts.models import Host

class HostLog(MiddlewareMixin):


    def process_request(self,request):
        pass


    def process_view(self, request, view_func, view_func_args, view_func_kwargs):
        # host edit old
        self.host_modify = {}
        if request.method == 'POST' and request.path[:-2] == '/hosts/edit/':
            before_h_id = request.POST.get('h_ip')
            print (before_h_id)
            before_host_obj = Host.objects.filter(h_ip=before_h_id).values()
            self.host_modify['before_modify'] = before_host_obj[0]

        # host delete
        if request.method == 'GET' and request.path == '/hosts/del/':
            self.host_del = {}
            req_ip = request.GET.get('hip',None)
            del_u_name = request.session['username']
            del_host_obj = Host.objects.filter(h_ip=req_ip).values()
            self.host_del['delete'] = del_host_obj[0]
            del_temp = {'log_type':'host','module':'delete','status':0,
                    'user':del_u_name,'description':self.host_del}
            models.PlatformLog.objects.create(**del_temp)

    def process_response(self, request,response):
        # host add
        if request.method == 'POST' and request.path == '/hosts/add/':
            add_h_name = request.POST.get('h_name')
            add_h_ip = request.POST.get('h_ip')
            add_u_name = request.session['username']
            add_temp = {'log_type':'host','module':'add','status':0,
                    'user':add_u_name,'description':{'name':add_h_name,'ip':add_h_ip}}
            models.PlatformLog.objects.create(**add_temp)
        # host edit new
        if request.method == 'POST' and request.path[:-2] == '/hosts/edit/':
            after_h_name = request.POST.get('h_name')
            after_h_ip = request.POST.get('h_ip')
            after_h_id = request.path[12:-1]
            after_u_name = request.session['username']
            self.host_modify['after_modify'] = {'h_id':after_h_id,'h_ip':after_h_ip,'h_name':after_h_name}
            after_temp = {'log_type':'host','module':'modify','status':0,
                    'user':after_u_name,'description':self.host_modify}
            models.PlatformLog.objects.create(**after_temp)


        return response


class UserLog(MiddlewareMixin):


    def process_request(self,request):
        pass

    def process_view(self, request, view_func, view_func_args, view_func_kwargs):
        pass

    def process_response(self, request, response):
        # user login
        if request.method == 'POST' and request.path == '/accounts/login/':
            if request.session.get('is_login'):
                login_u_name = request.session['username']
                login_REMOTE_IP = request.META['REMOTE_ADDR']
                login_REMOTE_NAME = request.META['REMOTE_HOST']
                user_temp = {'log_type':'user','module':'login','status':0,
                            'user':login_u_name,
                            'description':{'remote_addr':login_REMOTE_IP,'remote_host':login_REMOTE_NAME}}
                models.PlatformLog.objects.create(**user_temp)
        return response