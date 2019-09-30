from rest_framework import serializers
from assets.models import Asset,Server



class AssetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ('id', 'asset_type', 'name', 'sn', 'business_unit', 'status',
                  'manufacturer', 'manage_ip', 'tags', 'admin', 'idc',
                  'contract', 'purchase_day', 'expire_day', 'price', 'approved_by',
                  'memo', 'c_time', 'm_time',)

    def create(self, data):
        if(data.get('sn')):
            # assets_data = data.pop('assets')
            print (data)
            assets = Asset.objects.create(**data)
            print (assets)
        else:
            assets = Asset()
        # data['assets'] = assets;
        server = Server.objects.create(**{'asset':assets})
        return server