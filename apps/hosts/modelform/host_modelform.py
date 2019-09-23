from hosts import models
from django.forms import ModelForm
from django.forms import widgets
# from django.forms import fields

class Host_MF(ModelForm):
    class Meta:
        model = models.Host

        fields = "__all__"
        labels = {
            'h_name':'主机名',
            'h_ip':'IP地址',

        }
        widgets = {
            'h_name': widgets.Input(attrs={"class":'form-control','placeholder':"请输入主机名","type":"text"}),
            'h_ip': widgets.Input(attrs={"class":'form-control','placeholder':"请输入IP地址","type":"text"}),
        }


class HostGroup_MF(ModelForm):
    class Meta:
        model = models.HostGroup

        fields = "__all__"
