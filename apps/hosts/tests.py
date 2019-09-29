import sys
import os
from django.conf import settings
pwd = os.path.dirname(os.path.realpath(__file__))



sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fdommp.settings")

import django
django.setup()

from api.serializers import AssetsSerializer
from assets.models import Asset

snippets = Asset.objects.all()
serializer = AssetsSerializer(snippets, many=True)
print (serializer.data)


