from django.urls import path,re_path
from databases import views
# from .views import article_add,upload_image,article_edit,article_index

app_name = 'databases'

urlpatterns = [
    # url(r'^config/$', views.DatabaseConfigs.as_view()),
    path('manage/', views.DatabaseManage.as_view(),name='db_manage'),
    # url(r'^users/$', views.DatabaseUsers.as_view()),
    # url(r'^query/$', views.DatabaseQuery.as_view()),
    # url(r'^execute/histroy/$', views.DatabaseExecuteHistroy.as_view()),
]