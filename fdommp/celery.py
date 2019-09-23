# from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fdommp.settings')

broker = 'redis://127.0.0.1:6379/5'
backend = 'redis://127.0.0.1:6379/6'

app = Celery('fdommp',broker=broker,backend=backend)

app.autodiscover_tasks(settings.INSTALLED_APPS)
# app.conf.timezone = 'Asia/Shanghai'
app.conf.update(timezone= 'Asia/Shanghai',
                task_time_limit = 120,
                worker_max_tasks_per_child = 40)





if __name__ == '__main__':
    app.start()