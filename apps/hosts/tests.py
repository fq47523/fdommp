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

import  json
from assets.dao import AssetManage
from django.core import serializers
from assets.models import Tag,Asset

ass = Asset()
tag = Tag.objects.all()
aa = AssetManage()
cc = aa.api_meun()
# ret = serializers.serialize("json",)
dd = {'asset_type': 'server', 'sn': 'ubuntu', 'name': 'server: ubuntu', 'tags':[1,2,3]}
Asset.objects.filter(sn='ubuntu').update(**dd)








