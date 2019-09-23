"""fdommp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,re_path
from hosts import views_zdh
from hosts import views_host

app_name = 'hosts'

urlpatterns = [
    path('list/', views_host.host, name='hostlist'),
    path('add/', views_host.host_add, name='hostadd'),
    re_path('edit/(?P<h_id>\d+)/', views_host.host_edit, name='hostedit'),
    path('del/', views_host.host_del, name='hostdel'),
    path('hostgroup/', views_host.hostgroup,name='hostgroup'),
    path('automate_shell/', views_zdh.automate_shell, name='shell'),
    re_path('automate_shell_result/(?P<ansible_type>\w+)/', views_zdh.automate_shell_result, name='shell_result'),
    path('automate_playbook/', views_zdh.automate_playbook, name='playbook'),
    re_path('automate_playbook_result/(?P<ansible_type>\w+)/', views_zdh.automate_playbook_result, name='playbook_result'),
    path('automate_crontab/', views_zdh.automate_crontab, name='crontab_list'),
    path('automate_crontab_add/', views_zdh.automate_crontab_add, name='crontab_add'),
    re_path('automate_crontab_add_host/(?P<job_name>\w+)/', views_zdh.automate_crontab_add_host, name='crontab_add_host'),
    re_path('automate_crontab_edit/(?P<job_name>\w+)/', views_zdh.automate_crontab_edit, name='crontab_edit'),
    path('automate_crontab_del/', views_zdh.automate_crontab_del, name='crontab_del'),
    re_path('automate_crontab_host/(?P<h_id>\d+)/', views_zdh.automate_crontab_host, name='crontab_host'),
    re_path('automate_crontab_host_action/', views_zdh.automate_crontab_host_action, name='crontab_host_action'),

]
