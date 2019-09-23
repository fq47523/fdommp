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
from confd import views

app_name = 'confd'

urlpatterns = [
    path('list/', views.confd_list,name='confd_list'),
    path('add/', views.confd_add,name='confd_add'),
    re_path('edit/(?P<confd_id>\d+)/',views.confd_edit,name='confd_edit'),
    path('init/',views.confd_init,name='confd_init'),
    path('del/',views.confd_del,name='confd_del'),
    path('rollback/',views.confd_rollback,name='confd_rollback')
]
