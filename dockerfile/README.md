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
  * 下载fdommp-dockerfile 到你的任意目录
  * 运行./init.py  (默认手动下载代码zip文件到"你的路径/dockerfile/fdommp-master.zip",或修改注释自动下载)
  * app镜像可能需要一段时间
  
运行容器<br>
  >docker run --name fd-db -d --net fd-net -p 3307:3306 fdommp-db <br> 
  >docker run --name fd-app -d --net fd-net fdommp-app <br> 
  >docker run --name fd-nginx -d --net fd-net -p 8080:80 fdommp-nginx  <br> 
  
或其他编排工具管理
  
