import  requests
from django.conf import settings
# from ops import models


class Zabbix_API(object):
    def __init__(self):
        self.url = settings.FD_ZABBIX_API_URL
        self.user = settings.FD_ZABBIX_USER
        self.pwd = settings.FD_ZABBIX_PASSWD
        self.token_id = 'e253f73ca7559cc82674241f807afbe3'

    def  UserLogin(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.user,
                "password": self.pwd
            },
            "id": 0,
        }
        return  self.Req_Post(data)

    def Req_Post(self,data):
        try:
            r = requests.post(self.url, json=data)
            rr = r.json()
        except Exception as e:
            print (e)
            return False
        return rr['result']


    def user_get(self):
        data = {
            "jsonrpc": "2.0",
            "method": "user.get",
            "params": {
                "output": "extend"
            },
            "auth": self.token_id,
            "id": 0
        }
        return self.Req_Post(data)

    def host_get(self): # 获取主机id，主机名，ip地址
        data = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                 "output": [
                 "hostid",
                 "host"
                ],
                "selectInterfaces": [
                "ip"
                ]
            },
            "auth": self.token_id,
            "id": 0
        }
        return self.Req_Post(data)

    def itemid_get(self,host_ids,item_key):
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":"itemid",
                "hostids":host_ids,
                "search": {
                    "key_": item_key
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)

    def history_get(self,item_ids,limit,sort='DESC'):
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 3,
                "itemids": item_ids,
                "sortfield": "clock",
                "sortorder": sort,
                "limit": limit
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)

    def host_mem_total(self,hostids):   # 单个主机内存总量（字节）
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["lastvalue"],
                "hostids":hostids,
                "search": {
                    "key_": "vm.memory.size[total]"
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)

    def host_disk_total(self,hostids):   # 单个主机磁盘总量（字节）
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["lastvalue"],
                "hostids":hostids,
                "search": {
                    "key_": "vfs.fs.size[/,total]"
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)





    def za_agent_action(self,hostids):  # za客户端状态：value 0 在线,1不在线
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output":["value"],
                "hostids":hostids,
                "filter":{"description":"Zabbix agent on {HOST.NAME} is unreachable for 5 minutes"}
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)

    def za_agent_cpu_system(self,hostids): # 使用主机cpu（system）：lastvalue的浮点数值
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["lastvalue"],
                "hostids":hostids,
                "search": {
                    "key_": "system.cpu.util[,system]"
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)


    def za_agent_cpu_user(self,hostids): # 使用主机cpu（user)：lastvalue的浮点数值
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["lastvalue"],
                "hostids":hostids,
                "search": {
                    "key_": "system.cpu.util[,user]"
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)

    def za_agent_mem(self,hostids): # 主机内存（可用）：lastvalue值整数/1024 / 1024 / 1024 得到浮点取.后2位
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["lastvalue"],
                "hostids":hostids,
                "search": {
                    "key_": "vm.memory.size[available]"
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)

    def za_agent_disk(self,hostids): # 主机磁盘（可用）：lastvalue值整数/1024 / 1024 / 1024 得到浮点取.后2位
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["lastvalue"],
                "hostids":hostids,
                "search": {
                    "key_": "vfs.fs.size[/,used]"
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)


    def za_agent_mysql(self, hostids):  #mysql 模板中mysql存活状态： 0 is down 1 ok
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output":["lastvalue"],
                "hostids":hostids,
                "search": {
                    "key_": "mysql.ping"
                }
            },
            "id": 0,
            "auth": self.token_id,
        }
        return self.Req_Post(data)

if __name__ == '__main__':
    # tonken = Zabbix_API()
    # print (tonken.UserLogin())

    zabbix_init = Zabbix_API()
    hostid_list = zabbix_init.host_get()
    za_list = []
    for i in hostid_list:
        # 遍历za主机的id
        za_action = zabbix_init.za_agent_action(i['hostid'])
        za_cpu_system = zabbix_init.za_agent_cpu_system(i['hostid'])
        za_cpu_user = zabbix_init.za_agent_cpu_user(i['hostid'])
        za_mem_available = zabbix_init.za_agent_mem(i['hostid'])
        za_mem_total = zabbix_init.host_mem_total(i['hostid'])
        za_disk = zabbix_init.za_agent_disk(i['hostid'])


        i['za_action'] = za_action[0]['value']
        i['za_cpu'] = round(float(za_cpu_system[0]['lastvalue']) + float(za_cpu_user[0]['lastvalue']), 2)
        i['za_mem'] = round((int(za_mem_total[0]['lastvalue']) - int(za_mem_available[0]['lastvalue']))/ 1024 / 1024 / 1024, 2)
        i['za_disk'] = round(int(za_disk[0]['lastvalue']) / 1024 / 1024 / 1024, 2)


        # for action_res in za_action:
        #     i['za_action'] = int(action_res['value'])
        #
        # for cpu_res in za_cpu:
        #     i['za_cpu'] = round(float(cpu_res['lastvalue']), 2)
        #
        # for mem_res in za_mem_available:
        #     temp_za_mem_available = round(int(mem_res['lastvalue']) / 1024 / 1024 / 1024, 2)
        #
        # for mem_res in za_mem_total:
        #     i['za_mem'] = round(int(mem_res['lastvalue']) / 1024 / 1024 / 1024, 2)
        #
        #
        # for disk_res in za_disk:
        #     i['za_disk'] = round(int(disk_res['lastvalue']) / 1024 / 1024 / 1024, 2)

        za_list.append(i)

    print (za_list)