from django.urls import path,re_path
from databases import views
# from .views import article_add,upload_image,article_edit,article_index

app_name = 'databases'

urlpatterns = [
    # url(r'^config/$', views.DatabaseConfigs.as_view()),
    path('manage/', views.DatabaseManage.as_view(),name='db_manage'),
    # path(r'^users/$', views.DatabaseUsers.as_view()),
    path('query/', views.DatabaseQuery.as_view(),name='db_query'),
    # url(r'^execute/histroy/$', views.DatabaseExecuteHistroy.as_view()),
    path('soarindex/',views.SoarIndex,name='db_soarindex'),
    path('soarcmd/',views.SoarCmd,name='db_soarcmd')
]