import sys
import os
from django.conf import settings
pwd = os.path.dirname(os.path.realpath(__file__))



sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fdommp.settings")

import django
django.setup()


# from  utils._get_config import ConfigR
#
# f = ConfigR()
# print (f.sections_value('debug','DEBUG'))


import re

a = 'attachment; filename=fdommp-master.zip'
print (re.findall('filename=(.*)',a))

