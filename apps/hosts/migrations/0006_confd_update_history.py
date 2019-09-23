# Generated by Django 2.1.3 on 2019-07-26 10:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0005_confd_conf_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confd_Update_History',
            fields=[
                ('cuh_id', models.AutoField(primary_key=True, serialize=False)),
                ('conf_id', models.IntegerField()),
                ('conf_ip', models.GenericIPAddressField()),
                ('conf_server', models.CharField(max_length=32)),
                ('backup_ver', models.IntegerField()),
                ('backup_path', models.CharField(max_length=128)),
                ('target_path', models.CharField(max_length=64)),
                ('backup_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
