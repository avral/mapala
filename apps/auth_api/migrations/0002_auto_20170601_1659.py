# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-01 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blockchain',
            name='blockchain',
        ),
        migrations.RemoveField(
            model_name='blockchain',
            name='master_node',
        ),
        migrations.RemoveField(
            model_name='user',
            name='auto_update_position',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bitcoin_address',
        ),
        migrations.RemoveField(
            model_name='user',
            name='contacts',
        ),
        migrations.RemoveField(
            model_name='user',
            name='languages',
        ),
        migrations.RemoveField(
            model_name='user',
            name='message',
        ),
        migrations.RemoveField(
            model_name='user',
            name='now_not_in_position',
        ),
        migrations.RemoveField(
            model_name='user',
            name='posting_key',
        ),
        migrations.AddField(
            model_name='blockchain',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='blockchain',
            name='wws',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='blockchain',
            name='locale',
            field=models.CharField(choices=[('ru', 'Русский'), ('en', 'English')], max_length=5, null=True),
        ),
    ]