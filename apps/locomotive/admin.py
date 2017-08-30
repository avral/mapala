from django.contrib import admin

from apps.locomotive.models import LocoMember

admin.site.register([
    LocoMember
])
