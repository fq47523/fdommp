from rest_framework import serializers
from assets.models import Asset

class AssetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ('id', 'asset_type', 'name', 'sn', 'business_unit', 'status',
                  'manufacturer', 'manage_ip', 'tags', 'admin', 'idc',
                  'contract', 'purchase_day', 'expire_day', 'price', 'approved_by',
                  'memo', 'c_time', 'm_time',)

