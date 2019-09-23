import sys
import os,time

# 获取当前文件的目录
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fdommp.settings")

import django
django.setup()


from hosts import models
from api.utils.zabbix_api import Zabbix_API
import time

#celery定时器探测
# def host_zabbix():
#     '''
#     获取zabbix客户端中主机的存活，cpu，men，disk剩余量,并写入数据库
#     :return:
#     '''
#     zabbix_init = Zabbix_API()
#     hostid_list = zabbix_init.host_get()
#     za_list = []
#     for i in hostid_list:
#         # 遍历za主机的id
#         za_action = zabbix_init.za_agent_action(i['hostid'])
#         za_cpu = zabbix_init.za_agent_cpu(i['hostid'])
#         za_mem = zabbix_init.za_agent_mem(i['hostid'])
#         za_disk = zabbix_init.za_agent_disk(i['hostid'])
#
#         for action_res in za_action:
#             i['za_action'] = int(action_res['value'])
#
#         for cpu_res in za_cpu:
#             i['za_cpu'] = round(float(cpu_res['lastvalue']), 2)
#
#         for mem_res in za_mem:
#             i['za_mem'] = round(int(mem_res['lastvalue']) / 1024 / 1024 / 1024, 2)
#
#         for disk_res in za_disk:
#             i['za_disk'] = round(int(disk_res['lastvalue']) / 1024 / 1024 / 1024, 2)
#         za_list.append(i)
#
#     for za_host in za_list: # 遍历拼接好的za客户端数据,列表类型
#
#         if za_host['za_action'] == 0:   # 0:活
#             host_obj = models.Host.objects.filter(h_ip=za_host['interfaces'][0]['ip']).first()
#             if host_obj:
#                 hz_obj = models.Host_zabbix.objects.filter(za_ip=za_host['interfaces'][0]['ip'])
#                 if not hz_obj:
#                     models.Host_zabbix.objects.create(
#                         za_action=za_host['za_action'],
#                         za_cpu=za_host['za_cpu'],
#                         za_mem=za_host['za_mem'],
#                         za_disk=za_host['za_disk'],
#                         h_extend=host_obj,
#                         za_ip=za_host['interfaces'][0]['ip']
#                     )
#                 else:
#                     models.Host_zabbix.objects.filter(za_ip=za_host['interfaces'][0]['ip']).update(
#                         za_action=za_host['za_action'],
#                         za_cpu=za_host['za_cpu'],
#                         za_mem=za_host['za_mem'],
#                         za_disk=za_host['za_disk']
#                     )
#             else:
#                 pass
#         elif za_host['za_action'] == 1: #1：死
#             host_obj = models.Host.objects.filter(h_ip=za_host['interfaces'][0]['ip']).first()
#             if host_obj:
#                 hz_obj = models.Host_zabbix.objects.filter(za_ip=za_host['interfaces'][0]['ip'])
#                 if not hz_obj:
#                     models.Host_zabbix.objects.create(
#                         za_action=za_host['za_action'],
#                         za_cpu=0,
#                         za_mem=0,
#                         za_disk=0,
#                         h_extend=host_obj,
#                         za_ip=za_host['interfaces'][0]['ip']
#                     )
#                 else:
#                     models.Host_zabbix.objects.filter(za_ip=za_host['interfaces'][0]['ip']).update(
#                         za_action=za_host['za_action'],
#                         za_cpu=0,
#                         za_mem=0,
#                         za_disk=0,
#                     )
# host_zabbix()


# class server_zabbix(object):
#     '''
#     填充ops平台中的主机对应的服务状态，从za服务里面的获取
#     '''
#     def __init__(self):
#         self.zabbix_init = Zabbix_API()
#         self.za_host_dic = self.zabbix_init.host_get()
#
#     def za_zabbix_server(self):
#         server_obj = models.Service.objects.all()
#         for i in server_obj.filter(s_name='mysqld'):
#             for ii in i.h_server.all():
#                 for iii in self.za_host_dic:
#                     if ii.h_ip == iii['interfaces'][0]['ip']:
#                         host_obj = models.Host.objects.filter(h_ip=iii['interfaces'][0]['ip']).first()
#                         # print (ii,iii['interfaces'][0]['ip'],self.zabbix_init.za_agent_mysql(iii['hostid']))
#                         Service_zabbix_mysqld = self.zabbix_init.za_agent_mysql(iii['hostid'])
#
#                         Service_zabbix_obj = models.Service_zabbix.objects.filter(za_ip=iii['interfaces'][0]['ip'])
#                         if not Service_zabbix_obj:
#
#                             models.Service_zabbix.objects.create(za_ip=iii['interfaces'][0]['ip'],
#                                                                  za_mysqld=Service_zabbix_mysqld[0]['lastvalue'] if Service_zabbix_mysqld else 999,
#                                                                  h_extend=host_obj)
#                         else:
#                             models.Service_zabbix.objects.filter(za_ip=iii['interfaces'][0]['ip']).update(
#                                 za_mysqld=Service_zabbix_mysqld[0]['lastvalue'] if Service_zabbix_mysqld else 999
#                             )






# 重写，直接统计数据库
class za_dashboard_data(object):
    '''
    dashboard页表盘数据源
    '''
    def __init__(self):
        self.zabbix_init = Zabbix_API()
        self.za_host_dic = self.zabbix_init.host_get()
        self.za_host = models.Host_zabbix.objects.filter(za_action=0).values('za_ip')

    def total_cpu(self):
        host_on_line_obj = models.Host_zabbix.objects.filter(za_action=0).count()

        count_res = int(100 * host_on_line_obj )

        return count_res


    def total_mem(self):
        count = 0
        count_list = []
        for k in self.za_host_dic:

            za_host_ip = [i['za_ip'] for i in self.za_host]
            if k['interfaces'][0]['ip'] in za_host_ip:
                host_mem_total =  self.zabbix_init.host_mem_total(k['hostid'])
                # print (host_mem_total[0])
                count_list.append(host_mem_total[0])
        for i in count_list:
            count += int(i["lastvalue"])
        # print ('mem:',count)
        return count

    def total_disk(self):
        count = 0
        count_list = []
        for k in self.za_host_dic:
            za_host_ip = [i['za_ip'] for i in self.za_host]
            if k['interfaces'][0]['ip'] in za_host_ip:
                host_mem_total = self.zabbix_init.host_disk_total(k['hostid'])
                count_list.append(host_mem_total[0])
        for i in count_list:
            count += int(i["lastvalue"])
        count_res = int(count / 1024 / 1024 /1024)
        # print ('disk:',count_res)
        return count_res

    def total_net(self,date_num,type_key):

        '''
        :param date_num: N分钟，最新1分钟
        :param type_key: zabbix-item下面的key类型
        :return:
        '''

        history_total = []  # 存放不同主机流量


        history_set = []    # 叠加每台主机流量集合

        for host_id in self.za_host_dic:

            za_host_ip = [i['za_ip'] for i in self.za_host]
            if host_id['interfaces'][0]['ip'] in za_host_ip:
                itemid_list = self.zabbix_init.itemid_get(host_id['hostid'], type_key)
                history_list = self.zabbix_init.history_get(itemid_list[0]["itemid"], date_num)
                # print (itemid_list,history_list)
                if history_list:
                # print (history_list)
                    history_net = []
                    history_date = []  # 存放一份流量的日期
                    for history_obj in history_list:
                        history_net.append(int(history_obj['value']))
                        history_date.append(time.strftime("%H:%M:%S",time.localtime(int(history_obj['clock']))))
                    history_total.append(history_net)

                else:
                    pass



        for i_count in range(date_num):

            count = 0
            for i in history_total:
                # print (i,i[i_count])
                count += (int(i[i_count]))
            history_set.append(count)

        history_res = {}
        history_res['date'] = history_date[::-1]
        history_res['value'] = history_set[::-1]
        return history_res




# test = za_dashboard_data()
# print ('in',test.total_net(5,'net.if.in'))
# print ('out',test.total_net(5,'net.if.out'))