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

ass = Asset()
for i in Asset.asset_type_choice:
    print (i[0],i[1])

