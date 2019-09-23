from hosts import models

from api.utils.ansible_api import *
import json

class ServiceHealth(object):
    def __init__(self,servername,ip=[]):
        self.servicename = servername
        self.ip = ip

    def status_init(self):
        rbt = ANSRunner([])
        rbt.run_model(host_list=self.ip, module_name='shell', module_args='ps -ef  | grep -w {} | grep -v grep | wc -l'.format(self.servicename))
        data = rbt.get_model_result()
        #print(json.dumps(data, indent=4))
        if data['success']:
            for k,v in data['success'].items():
                ip = str(k)
                stdout_code = int(v['stdout'])

                if stdout_code > 0:
                    models.Service_Status.objects.create(server_name=self.servicename,
                                                         server_host=ip.replace('_','.'),
                                                         server_status=1
                                                         )
                elif stdout_code == 0:
                    models.Service_Status.objects.create(server_name=self.servicename,
                                                         server_host=ip.replace('_', '.'),
                                                         server_status=2
                                                         )
        if data['failed']:
            for k,v in data['failed'].items():
                ip = str(k)
                models.Service_Status.objects.create(server_name=self.servicename,
                                                     server_host=ip.replace('_', '.'),
                                                     server_status=3
                                                     )
        if data['unreachable']:
            for k,v in data['unreachable'].items():
                ip = str(k)
                models.Service_Status.objects.create(server_name=self.servicename,
                                                     server_host=ip.replace('_', '.'),
                                                     server_status=4
                                                     )

    def status_get(self):
        rbt = ANSRunner([])
        rbt.run_model(host_list=self.ip, module_name='shell', module_args='ps -ef  | grep -w {} | grep -v grep | wc -l'.format(self.servicename))
        data = rbt.get_model_result()


        if data['success']:
            for k,v in data['success'].items():
                ip = str(k)
                stdout_code = int(v['stdout'])
                print (k,v)
                if stdout_code > 0:
                    models.Service_Status.objects.filter(server_name=self.servicename,
                                                         server_host=ip.replace('_','.'),
                                                         ).update(server_status=1)
                elif stdout_code == 0:
                    models.Service_Status.objects.filter(server_name=self.servicename,
                                                         server_host=ip.replace('_', '.'),
                                                         ).update(server_status=2)

        if data['failed']:
            for k,v in data['failed'].items():
                ip = str(k)
                stdout_code = int(v['stdout'])

                models.Service_Status.objects.filter(server_name=self.servicename,
                                                         server_host=ip.replace('_', '.'),
                                                         ).update(server_status=3)

        if data['unreachable']:

            for k,v in data['unreachable'].items():
                ip = str(k)


                models.Service_Status.objects.filter(server_name=self.servicename,
                                                         server_host=ip.replace('_', '.'),
                                                         ).update(server_status=4)