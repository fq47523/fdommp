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

from hosts.models import Service
from assets.models import Asset

a = ['<服务器>  server: ubuntu','<服务器>  server: zabbix']

c = [i.split()[2]  for i in a]
print (c)
dd = [i.manage_ip for i in Asset.objects.filter(sn__in=c)]
print (dd)