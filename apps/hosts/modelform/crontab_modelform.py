from hosts import models
from django.forms import ModelForm
from django.forms import widgets


class Crontab_MF(ModelForm):
    class Meta:
        model = models.Crontab
        fields = "__all__"
        labels = {
            'jobname':'任务名称',
            'minute':'分',
            'hour':'时',
            'day':'日',
            'month':'月',
            'weekday':'周',
            'jobcli':'命令',
            'cron_host':'host'

        }

        widgets = {
            'jobname':widgets.Input(attrs={"class":'form-control','placeholder':"请输入服务名","type":"text"}),
            'minute': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'hour': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'day': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'month': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'weekday': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'jobcli': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'cron_host':widgets.SelectMultiple(attrs={'class':'form-control select2','multiple':'multiple'}),

        }



class Crontab_Edit_MF(ModelForm):
    class Meta:
        model = models.Crontab
        exclude = ['cron_host']
        labels = {
            'jobname':'任务名称',
            'minute':'分',
            'hour':'时',
            'day':'日',
            'month':'月',
            'weekday':'周',
            'jobcli':'命令',


        }

        widgets = {
            'jobname':widgets.Input(attrs={"class":'form-control','placeholder':"请输入服务名","type":"text",'readonly':'readonly'}),
            'minute': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'hour': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'day': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'month': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'weekday': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),
            'jobcli': widgets.Input(attrs={"class": 'form-control', 'placeholder': "请输入服务名", "type": "text"}),


        }

class Crontab_Add_Host_MF(ModelForm):
    class Meta:
        model = models.Crontab
        fields = ['cron_host']
        labels = {

            'cron_host':'host'


        }

        widgets = {

            'cron_host':widgets.CheckboxSelectMultiple(),


        }

