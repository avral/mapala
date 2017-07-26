# coding:utf-8
# всё далее идет для allauth
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_migrate




class DemoConfig(AppConfig):
    name = 'backend'
    verbose_name = _('backend')

    # def ready(self):
    #     post_migrate.connect(setup_dummy_social_apps, sender=self)
