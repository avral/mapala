# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-14 19:28
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permlink', models.CharField(blank=True, max_length=512, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Ошибка публикации'), (1, 'Публикуется'), (2, 'Опубликовано')], default=1)),
                ('body', models.TextField(null=True)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='MasterTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(default='', max_length=1024)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pages.MasterTag', verbose_name='Тэг дерева')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('permlink', models.SlugField(max_length=255, null=True, unique=True)),
                ('parent_permlink', models.CharField(blank=True, max_length=1000, null=True)),
                ('body', models.TextField()),
                ('total_payout_value', models.CharField(blank=True, max_length=200, null=True)),
                ('total_pending_payout_value', models.CharField(blank=True, max_length=200, null=True)),
                ('actual_price', models.FloatField(blank=True, null=True)),
                ('locale', models.CharField(choices=[('ru', 'Русский'), ('en', 'English')], default='ru', max_length=100)),
                ('links', models.CharField(blank=True, max_length=100000, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Ошибка публикации'), (1, 'Публикуется'), (2, 'Опубликовано')], default=0)),
                ('position', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('position_text', models.CharField(max_length=1000)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to=settings.AUTH_USER_MODEL)),
                ('images', models.ManyToManyField(blank=True, to='pages.Image')),
                ('master_tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pages.MasterTag')),
            ],
        ),
        migrations.CreateModel(
            name='Parser_settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_proceeded_block', models.BigIntegerField(default=0)),
                ('blockchain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_api.BlockChain')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(blank=True, to='pages.Tag'),
        ),
        migrations.AddField(
            model_name='page',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='pages_vote', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='pages.Page'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='pages.Comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='voters',
            field=models.ManyToManyField(blank=True, related_name='voters', to=settings.AUTH_USER_MODEL),
        ),
    ]
