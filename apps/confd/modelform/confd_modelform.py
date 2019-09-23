from hosts.models import Confd
from django.forms import ModelForm
from django.forms import widgets

class Confd_MF(ModelForm):
    class Meta:
        model = Confd
        fields = ['conf_name','conf_path','conf_service','conf_host']
        labels = {
            'conf_name':'配置名称',
            'conf_path':'配置路径',
            'conf_service':'配置类型',
            'conf_host':'配置主机'
        }

        widgets = {
            'conf_name': widgets.Input(attrs={"class": 'form-control', 'placeholder': "conf_name", "type": "text"}),
            'conf_path': widgets.Input(attrs={"class": 'form-control', 'placeholder': "conf_path", "type": "text"}),
            'conf_service': widgets.SelectMultiple(attrs={'class': 'form-control select2', 'multiple': 'multiple'}),
            'conf_host': widgets.SelectMultiple(attrs={'class': 'form-control select2', 'multiple': 'multiple'}),
        }