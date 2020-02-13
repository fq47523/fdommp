#!/bin/bash

docker -v
if [ "$?" -ne 0 ];then
echo " stop,stop!!"
exit 5
fi




dfpwd=`pwd`

fd_nginx_s=$dfpwd'/dockerfile/fdommp-nginx/Dockerfile'
fd_app_s=$dfpwd'/dockerfile/fdommp-app/Dockerfile'
fd_db_s=$dfpwd'/dockerfile/fdommp-db/Dockerfile'
build_d=$dfpwd'/dockerfile/'






    
docker build -t fdommp-nginx -f "$fd_nginx_s" "$build_d"
#print ('---------------------------build nginx-----------------------------')
#for i in exec_nginx.stdout.read().decode().split('\n'):print (i)
docker build -t fdommp-app -f "$fd_app_s" "$build_d"
#print ('---------------------------build app-----------------------------')
#for i in exec_app.stdout.read().decode().split('\n'):print (i)

docker build -t fdommp-db -f "$fd_db_s" "$build_d"
#print ('---------------------------build db-----------------------------')
#for i in exec_db.stdout.read().decode().split('\n'):print (i)



  
