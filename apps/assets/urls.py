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
from assets import views

app_name = 'assets'

urlpatterns = [
    path('collect/',views.AutoAssetCreateOrUpdate.as_view()),
    path('list/', views.AssetView.as_view(),name='assets_list'),
    path('detail/',views.AssetDetailView.as_view(),name='assets_detail'),
    path('add/',views.AssetManualAdd.as_view(),name='assets_add'),
    path('sync/',views.AnsibleAssetCreateOrUpdate.as_view(),name='assets_sync'),


]
