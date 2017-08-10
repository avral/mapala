# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 12:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0012_auto_20170722_0035'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pages', '0008_page_meta'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='comment',
            unique_together=set([('author', 'permlink', 'page')]),
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('author', 'permlink', 'blockchain')]),
        ),
    ]
