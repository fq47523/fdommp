# Generated by Django 2.1.3 on 2019-07-29 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0006_confd_update_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='confd_update_history',
            name='conf_name',
            field=models.CharField(default='', max_length=32),
        ),
    ]
