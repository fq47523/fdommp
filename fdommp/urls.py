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
from django.contrib import admin
from .userlogin import ul_view
from django.urls import path,include,re_path
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token),
    re_path('^$', ul_view.Index.as_view()),
    re_path('^login/$', ul_view.login),
    re_path('^logout/$', ul_view.logout),
    path('accounts/', include('accounts.urls')),
    path('hosts/', include('hosts.urls')),
    path('service/', include('service.urls')),
    path('api/', include('api.urls')),
    path('logger/', include('logger.urls')),
    path('wssh/', include('webssh.urls')),
    path('confd/', include('confd.urls')),
    path('assets/',include('assets.urls')),
    re_path('^403/$', ul_view.Permission.as_view()),

]
