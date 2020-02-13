FROM python:3.6.6

# base 



COPY fdommp-plugins/app/requirement.txt /mnt
COPY fdommp-plugins/app/start.sh /mnt
COPY fdommp-plugins/app/sources.list /etc/apt
COPY fdommp-plugins/app/supervisord.conf /mnt
#COPY fdommp-plugins/app/user.json /mnt
#COPY fdommp-master.zip /mnt

RUN apt-get update \
 && apt-get install -y unzip supervisor sshpass && mkdir /mnt/fdommp



RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -r /mnt/requirement.txt -i https://mirrors.aliyun.com/pypi/simple/

# uwsgi 
#RUN groupadd -g 2001 uwsgi_group
#RUN useradd -u 2001 -g uwsgi_group uwsgi_user
#RUN chown -R 2001.2001 /mnt/

# code env
#ENV FDOMMP_RUN_ENV=PROD


WORKDIR /mnt

EXPOSE 8000

#CMD ["/bin/bash","start.sh"]
