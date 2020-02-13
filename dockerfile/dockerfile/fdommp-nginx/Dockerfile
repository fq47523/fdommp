FROM hub.c.163.com/library/nginx:1.13.0-alpine

COPY fdommp-plugins/nginx/fdommp.conf /etc/nginx/conf.d/
#ADD fdommp.tar /mnt
#ADD fdommp-master.zip  /mnt
#RUN unzip -q -d /mnt/  /mnt/fdommp-master.zip
RUN mkdir /mnt/fdommp && mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.bak && echo 'uwsgi_param  REMOTE_HOST        $remote_addr;' >> /etc/nginx/uwsgi_params
