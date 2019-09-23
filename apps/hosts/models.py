from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class Host(models.Model):
    h_id = models.AutoField(primary_key=True)
    h_name = models.CharField(max_length=16,unique=True)
    h_ip = models.GenericIPAddressField(max_length=32,unique=True)

    def __str__(self):
        return self.h_ip

class HostGroup(models.Model):
    hg_id = models.AutoField(primary_key=True)
    hg_name = models.CharField(max_length=16,unique=True)
    hg_h_r = models.ManyToManyField('Host')


class Host_zabbix(models.Model):
    za_ip = models.GenericIPAddressField(max_length=32,unique=True)
    za_action = models.IntegerField()
    za_cpu = models.FloatField()
    za_mem = models.FloatField()
    za_disk = models.FloatField()

    h_extend = models.ForeignKey('Host', to_field='h_id', default=999, on_delete=models.CASCADE)

class Service_zabbix(models.Model):
    za_ip = models.GenericIPAddressField(max_length=32, unique=True)
    h_extend = models.ForeignKey('Host', to_field='h_id', default=999, on_delete=models.CASCADE)
    za_mysqld = models.IntegerField(default=999)
    za_nginx = models.IntegerField(default=999)
    za_ewc = models.IntegerField(default=999)


class Service(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=16,unique=True)
    s_type = models.CharField(max_length=16)
    h_server = models.ManyToManyField('Host')

    def __str__(self):
        return self.s_name

class Service_Status(models.Model):
    # server_status  = 1：进程存在，2：进程不存在或软件没有安装
    id = models.AutoField(primary_key=True)
    server_name = models.CharField(max_length=64,default='')
    server_host = models.GenericIPAddressField(max_length=32)
    server_status = models.IntegerField()


class Crontab(models.Model):
    id = models.AutoField(primary_key=True)
    jobname = models.CharField(max_length=32,unique=True)
    minute = models.CharField(max_length=32)
    hour = models.CharField(max_length=32)
    day = models.CharField(max_length=32)
    month = models.CharField(max_length=32)
    weekday = models.CharField(max_length=32)
    jobcli = models.CharField(max_length=128)
    cron_host = models.ManyToManyField('Host')

class Crontab_Status(models.Model):
    # job_status  = 1.生效 2.暂停
    id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=64,default='')
    job_host = models.GenericIPAddressField(max_length=32)
    job_status = models.IntegerField()

class Confd(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(default=timezone.now)
    conf_name = models.CharField(max_length=64,unique=True)
    conf_path = models.CharField(max_length=64)
    current_ver = models.IntegerField(default=0)
    modified_ver = models.IntegerField(default=0)
    conf_host = models.ManyToManyField('Host')
    conf_service = models.ManyToManyField('Service')

class Confd_Update_History(models.Model):
    cuh_id = models.AutoField(primary_key=True)
    conf_id = models.IntegerField()
    conf_ip = models.GenericIPAddressField(max_length=32)
    conf_name = models.CharField(max_length=32)
    conf_server = models.CharField(max_length=32)
    backup_ver = models.IntegerField()
    backup_path = models.CharField(max_length=128)
    target_path = models.CharField(max_length=64)
    backup_date = models.DateTimeField(default=timezone.now)
