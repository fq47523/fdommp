from django.db import models

# Create your models here.
class PlatformLog(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    log_type = models.CharField(max_length=16)
    module = models.CharField(max_length=16)
    user = models.CharField(max_length=16,default='')
    status = models.IntegerField()
    description = models.CharField(max_length=128)