import sys
import os
from django.conf import settings
pwd = os.path.dirname(os.path.realpath(__file__))



sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fdommp.settings")

import django
django.setup()

from api.serializers import AssetsSerializer
from assets.models import Asset,Server

a = {'asset': {'asset_type': 'server', 'name': 'server: ios', 'sn': 'ios', 'business_unit': None, 'status': 0, 'manufacturer': 1, 'manage_ip': '192.168.79.122', 'admin': None, 'idc': None, 'contract': None, 'purchase_day': None, 'expire_day': None, 'price': None, 'approved_by': 1, 'memo': None}, 'sub_asset_type': 0, 'created_by': 'auto', 'hosted_on': None, 'model': 'VMware Virtual Platform', 'raid_type': None, 'username': None, 'passwd': None, 'sshport': '22', 'keyfile': None, 'sudo_passwd': None, 'kernel': None, 'selinux': None, 'os_type': 'Linux', 'os_distribution': 'Ubuntu', 'os_release': 'Ubuntu 16.04.6 LTS'}
print (a.pop('asset'))

