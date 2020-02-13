#!/usr/bin/env python3

try:
    import os,sys,subprocess
    from plugins.get_code import Getfile
except Exception as e:
    print ('not found model:',e)
    sys.exit(1)

git_url = 'https://codeload.github.com/fq47523/fdommp/zip/master'
pwd = os.path.dirname(os.path.realpath(__file__))
code_path = pwd+'/dockerfile/'

fd_nginx_s = pwd+'/dockerfile/fdommp-nginx/Dockerfile'
fd_app_s = pwd+'/dockerfile/fdommp-app/Dockerfile'
fd_db_s = pwd+'/dockerfile/fdommp-db/Dockerfile'
build_d = pwd+'/dockerfile/'



#docker_net_create = subprocess.Popen('docker network create --driver bridge fd-net',stdout=subprocess.PIPE,shell=True)
#print ('docker_net_create_ret: ',docker_net_create.stdout.read().decode().strip('\n'))
#docker_net_check = subprocess.Popen("docker network  ls | grep 'fd-net' > /dev/null  && echo 'success'",stdout=subprocess.PIPE,shell=True)
#docker_net_check_res = docker_net_check.stdout.read().decode()

#if docker_net_check_res.strip('\n') == 'success':

    #print ('---------------------------git pull code-----------------------------')
    #filename = Getfile(git_url).getfilename()
    #Getfile(git_url).downfile(code_path+filename)

    
exec_nginx = subprocess.Popen('docker build -t fdommp-nginx -f {} {}'.format(fd_nginx_s,build_d),stdout=subprocess.PIPE,shell=True)
print ('---------------------------build nginx-----------------------------')
for i in exec_nginx.stdout.read().decode().split('\n'):print (i)
    
exec_app = subprocess.Popen('docker build -t fdommp-app -f {} {}'.format(fd_app_s,build_d),stdout=subprocess.PIPE,shell=True)
print ('---------------------------build app-----------------------------')
for i in exec_app.stdout.read().decode().split('\n'):print (i)

exec_db = subprocess.Popen('docker build -t fdommp-db -f {} {}'.format(fd_db_s,build_d),stdout=subprocess.PIPE,shell=True)
print ('---------------------------build db-----------------------------')
for i in exec_db.stdout.read().decode().split('\n'):print (i)



   
