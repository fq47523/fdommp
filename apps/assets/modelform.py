from django.forms import ModelForm
from django.forms import widgets
from .models import Asset,Server

class GaiLanA(ModelForm):
    class Meta:
        model = Asset
        fields = ['asset_type','business_unit','manufacturer','manage_ip','idc','contract','price']


        widgets = {
            'asset_type':widgets.Select(),
            'business_unit':widgets.Select(),
            'manufacturer':widgets.Select(),
            'manage_ip':widgets.Input(),
            'idc':widgets.Select(),
            'contract':widgets.Select(),
            'price':widgets.Input(),

        }

class GaiLanB(ModelForm):
    class Meta:
        model = Server
        fields = ['username','passwd','sshport','sudo_passwd','keyfile']

        widgets = {
            'username': widgets.Input(),
            'passwd': widgets.Input(),
            'sshport': widgets.Input(),
            'sudo_passwd': widgets.Input(),
            'keyfile': widgets.Input(),

        }