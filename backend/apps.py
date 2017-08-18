from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DemoConfig(AppConfig):
    name = 'backend'
    verbose_name = _('backend')
