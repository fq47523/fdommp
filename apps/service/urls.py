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
from service import views

app_name = 'service'

urlpatterns = [
    path('list/', views.server, name='servicelist'),
    path('add/', views.server_add, name='serviceadd'),
    re_path('operation/(?P<sid>\d+)/(?P<type>\d+)/', views.server_operation, name='service_operation'),
    re_path('control_list/(?P<s_name>\w+)/(?P<s_type>\w+)/', views.server_control_list, name='service_control_list'),
    path('control_action/', views.server_control_action, name='service_control_action'),
    path('control_action_result/', views.server_control_action_result, name='service_control_action_result'),
    path('test/',views.testtpl,name='tpl')
]
