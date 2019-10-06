from rest_framework import serializers
from assets.models import Asset,Server



class AssetsSerializer(serializers.ModelSerializer):
    # c_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    # m_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Asset
        fields = ('id', 'asset_type', 'name', 'sn', 'business_unit', 'status',
                  'manufacturer', 'manage_ip', 'tags', 'admin', 'idc',
                  'contract', 'purchase_day', 'expire_day', 'price', 'approved_by',
                  'memo', 'c_time', 'm_time',)



class AssetsServerSerializer(serializers.ModelSerializer):
    asset = AssetsSerializer(required=False)

    class Meta:
        model = Server
        fields = ('id', 'asset', 'sub_asset_type', 'created_by', 'hosted_on', 'model',
                  'raid_type', 'username', 'passwd', 'sshport', 'keyfile',
                  'sudo_passwd', 'kernel', 'selinux', 'os_type', 'os_distribution',
                  'os_release')



    def create(self, data):
        print (data)
        if(data.get('asset')):
            assets_data = data.pop('asset')
            print ('assets_data:',assets_data)
            asset = Asset.objects.create(**assets_data)
            print ('asset_obj:',asset)
        else:
            asset = Asset()
        data['asset'] = asset
        server = Server.objects.create(**data)
        return server