# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-07 03:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20170606_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='permlink',
            field=models.SlugField(max_length=255, null=True),
        ),
    ]
