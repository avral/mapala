# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='chanel_link',
            field=models.CharField(max_length=200, null=True, verbose_name='чат афиши'),
        ),
    ]
