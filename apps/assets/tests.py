from django.test import TestCase
import  subprocess,os
# Create your tests here.



p = os.path.dirname(os.path.realpath(__file__)) + '/assetsdetail/'
cmd = 'ansible -i /home/fuqing/hosts -m setup --tree {} all'.format(p)
print (p)
r = subprocess.getstatusoutput(cmd)
# print (r)