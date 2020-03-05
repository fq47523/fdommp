# fdommp-dockerfile

准备工作
  * python3 安装
  * Ubuntu 16.04 docker 安装
  
  >由于apt官方库里的docker版本可能比较旧，所以先卸载可能存在的旧版本：<br> 
  $ sudo apt-get remove docker docker-engine docker-ce docker.io

  >更新apt包索引：<br> 
  $ sudo apt-get update

  >安装以下包以使apt可以通过HTTPS使用存储库（repository）：<br> 
  $ sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

  >添加Docker官方的GPG密钥：<br> 
  $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

  >使用下面的命令来设置stable存储库：<br> 
  $ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

  >再更新一下apt包索引：<br> 
  $ sudo apt-get update

  >安装最新版本的Docker CE：<br> 
  $ sudo apt-get install -y docker-ce
  
  * 镜像加速器<br>
  >vim /etc/docker/daemon.json
  
  >{"registry-mirrors": ["https://XXXXXXX.mirror.aliyuncs.com"]}

构建镜像
  * 代码路径/fdommp/dockerfile/build.sh  
  * 注意要在dockerfile下执行build,镜像中有上下文需求

修改路径
  * docker-compose.yml中的app,nginx本地代码卷挂载,容器路径不需要修改
  * ../conf/logger.ini中的日志路径为'/mnt/fdommp/logs/fdommp.log'

运行容器<br>
  * docker-compose up -d <br> 
  
已知问题
  * 首次启动后app容器需要多重启一次,因为mysql还未启动完成
  * 
  
使用你的地址＋8080端口,账户密码同为admin
