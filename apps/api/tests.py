from django.test import TestCase

# Create your tests here.

import requests
import json

# api

action = 'POST'
url1 = 'http://192.168.79.134:8080/api/service/action/'
url2 = 'http://192.168.79.134:8080/api/assetslist/'
data = {"action":
                    {"servicename":"zabbix_agentd",
                        "ip":"192.168.79.134",
		                "target":"stopped"
	                }
                }

headers ={
    "content-type":"application/json"
}
# req = requests.request(action,url1,headers=headers,data=json.dumps(data).encode("utf-8"))
# print (req.content)

# session

url = "http://192.168.79.134:8080/login/"
s = requests.session()  # 建立一个Session

response = s.post(url, data={"user": "fuqing", "pwd": "whstic@2019"})  # session登录网站
print (s.cookies)
response = s.post(url1,headers=headers,data=json.dumps(data))  # session浏览页面
response.encoding = "utf-8"
response_ret = response.json()
print (response_ret)
s.get("http://192.168.79.134:8080/logout/")


