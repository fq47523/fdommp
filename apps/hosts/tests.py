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
from assets.models import Tag,Asset,Server
from hosts.models import Service


# from utils.deploy.git import GitTools
#
# print (GitTools('/home/fuqing/PycharmProjects/fdommp').tag())

import subprocess,json

# ret = subprocess.getstatusoutput("echo 'select * from opsmanage.auth_user' | /opt/soar -online-dsn 'root:redhat@192.168.79.134:3307/opsmanage' -report-type json")
# print (json.loads(ret[1]))
# print (ret[1].split('\n'))


from databases import models
dd = {'db_env': 'ga', 'db_type': 'mysql', 'db_version': '5.7', 'db_business': '2', 'db_assets_id': '25', 'db_user': 'root', 'db_passwd': 'fdommp', 'db_port': '3307', 'db_mark': 'lll', 'db_rw': 'r/w', 'db_mode': 'single'}
models.DataBase_Server_Config.objects.create(**dd)