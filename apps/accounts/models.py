from django.db import models

# Create your models here.
class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    u_name = models.CharField(max_length=16,unique=True)
    u_pwd = models.CharField(max_length=16)