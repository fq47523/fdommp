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

from django.urls import re_path,path
from api import views
from api.apps_api import assets_api,service_api


app_name = 'api'

urlpatterns = [
    re_path('dashboard/(?P<type>\w+)/', views.dashboard_data, name='dashboard'),
    path("asset/meun/",assets_api.AssetsMeun.as_view(),name='api-assetsmeun'),
    path("asset/server/",assets_api.AssetsServerList.as_view(),name='api-assetslist'),
    re_path("asset/server/(?P<id>[0-9]+)/", assets_api.AssetsServerDetail.as_view(), name='api-assetaction'),
    path("service/action/",service_api.ServiceAction.as_view()),



]
