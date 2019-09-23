from hosts import models
from django.forms import ModelForm
from django.forms import widgets as ws
# from django.forms import fields




class Service_MF(ModelForm):
    class Meta:
        model = models.Service
        fields = "__all__"
        labels = {
            's_name':'服务名称',
            's_type':'服务类型',
            'h_server':'关联主机',
        }

        widgets = {
            's_name':ws.Input(attrs={"class":'form-control','placeholder':"请输入服务名","type":"text"}),
            's_type':ws.Input(attrs={"class":'form-control','placeholder':"请输入服务类型","type":"text"}),
            'h_server':ws.SelectMultiple(attrs={'class':'form-control select2','multiple':'multiple'}),


        }


