import  paramiko
"""连接到Linux主机并执行命令"""

class SSH_CLIENT(object):
    def __init__(self,ip_addr,Port,User,Passwd):
        self.client  = paramiko.SSHClient()
        self.ip_addr = ip_addr
        self.Port = Port
        self.User = User
        self.Passwd = Passwd
    def tactics(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    def conn(self):
        self.client.connect(self.ip_addr,port=self.Port,username=self.User,password=self.Passwd)

    def output(self,cmd):
        stdin,stdout,stderr = self.client.exec_command(cmd)
        ret, err = stdout.read().decode(), stderr.read().decode()
        rets = ret if ret else err
        self.client.close()
        return  rets

if __name__ == "__main__":



    test = ['192.168.79.141','192.168.79.133']
    for i in test:
        ip_addr = "192.168.79.133"
        Port = 22
        User = "root"
        Passwd = "redhat"

        a_client = SSH_CLIENT(ip_addr, Port, User, Passwd)
        a_client.tactics()
        a_client.conn()
        res = a_client.output("ansible {}  -m shell -a '/usr/local/ops/ops_test.sh ewc stopped'".format(i))
        print (res)


# print ("asdsad{} {} {}".format("a","b","c"))


#
# trantport = paramiko.Transport(ip_addr,Port)
# trantport.connect(username=User,password=Passwd)
#
# sftp = paramiko.SFTPClient.from_transport(trantport)
# #sftp.get("/root/digui.py","F:\\digui.py.new")
# sftp.put("F:\\digui.py.new","/root/digui.py.linux")
# trantport.close()