#!/bin/bash

if [ ! -d '/mnt/fdommp/apps/assets/migrations' ];then
dir='/mnt/fdommp/'
python "$dir"manage.py migrate && python "$dir"manage.py makemigrations databases && \
python "$dir"manage.py makemigrations assets && python "$dir"manage.py makemigrations hosts && \
python "$dir"manage.py makemigrations logger && python "$dir"manage.py makemigrations webssh && \
python "$dir"manage.py migrate && python "$dir"manage.py  loaddata /mnt/fdommp/user.json

fi

supervisord -c /mnt/supervisord.conf



#uwsgi --ini /mnt/fdommp/uwsgi-prod.ini --uid 2001 --gid 2001
uwsgi --ini /mnt/fdommp/uwsgi-prod.ini

