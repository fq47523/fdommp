项目起源
==
根据日常工作及以往项目经验,通过学习和借鉴写出的运维平台,已在50+的机器里面使用与测试,其中有些代码很笨拙,但随着经验提升相信会更好!

技术序列
==
### 前端
  * Bootstrap/JQuery/VUE
### 后台
  * Django/python3.6+
### 数据
  * Mysql 5.6 ++
  * Redis 3.2 ++
### 依赖
  * ElasticSearch，Logstash，Kafka，Filebeat，Zabbix

运行环境
==
### 容器运行
  * Docker version 19.03.2 ++
  * docker-compose version 1.8.0 ++
  * [安装传送门](https://github.com/fq47523/fdommp/tree/master/dockerfile)

功能清单
==
  ### 资产管理
      * 服务端拉取数据（手自一体），客户部部署脚本推送
  ### 主机管理
      * 运行情况
      * 网页SSH，SHELL,PLAYBOOK,动态CRONTAB
  ### 服务管理
      * 服务的状态
      * 服务的启停
  ### 配置管理
      * 在线编辑
      * 配置下发
      * 配置回滚
  ### 数据库管理
      * mysql运行情况
      * 表结构，SQL，binlog查询
      * 集成SOAR相关功能
  ### 日志管理
      * 平台运行日志
      * 基于ELF的错误日志
      
      
  
项目截图
==
![image](https://github.com/fq47523/fdommp/blob/master/FDpic/index.png)
![image](https://github.com/fq47523/fdommp/blob/master/FDpic/soar.png)
![image](https://github.com/fq47523/fdommp/blob/master/FDpic/eslog.png)

已知问题
==
* 资产删除时某些服务不能自动删除（crontab任务，服务任务及其他）
* 有些功能依赖zabbix，否则无法使用
* 前端没有统一按钮、弹窗、布局等
* 平台运行日志只有部分可以查询
* 部分代码没有将<script></script>移到独立js文件
* ansible配置文件没有进库
* 有些功能或代码块耦合度太高
* 其他隐藏问题

	
感谢作者
==
[welliamcao](https://github.com/welliamcao/OpsManage)
[xiyangxixian](https://github.com/xiyangxixian/soar-web)


