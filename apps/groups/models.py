from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    chat_link = models.CharField(max_length=200, null=True)
    logo = models.ImageField(upload_to='groups/', null=True, blank=True)

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __str__(self):
        return self.name
