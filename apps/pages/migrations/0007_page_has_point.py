# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-05 21:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20170626_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='has_point',
            field=models.BooleanField(default=False),
        ),
    ]
