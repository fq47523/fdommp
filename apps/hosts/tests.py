import sys
import os
from django.conf import settings
pwd = os.path.dirname(os.path.realpath(__file__))



sys.path.append(pwd + "../../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fdommp.settings")

import django
django.setup()

# git
# from git import  Repo
#
# url = 'https://github.com/fq47523/fdommp-dockerfile.git'
# gitpath = '/tmp/testgit'
#
#
# # Repo.clone_from(url, gitpath,multi_options=['--depth=1'])
# git_repo = Repo(gitpath)
# print (git_repo.branches)
# print (git_repo.tags)
from rest_framework_jwt.utils import  jwt_payload_handler
# from django.contrib.auth.models import User
# from rest_framework_jwt.settings import api_settings
# userobj = User.objects.get(username='fuqing')
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
# payload = jwt_payload_handler(userobj)
# token = jwt_encode_handler(payload)
# print (token)

from hosts.models import Host_zabbix
from assets.models import Asset

ass_obj = Asset.objects.filter(id=25).first()
print (type(ass_obj.manage_ip))
Host_zabbix.objects.update(
    za_ip= ass_obj.manage_ip,
    za_cpu= 0,
    za_mem= 1,
    za_disk= 0,
    za_action= 0,
    asset_extend= ass_obj
)

