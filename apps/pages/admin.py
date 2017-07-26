from django.contrib import admin
from apps.pages.models import Page, MasterTag, Tag, Image, Comment
from mptt.admin import MPTTModelAdmin


admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(MasterTag, MPTTModelAdmin)
admin.site.register(Image)
admin.site.register(Tag)
