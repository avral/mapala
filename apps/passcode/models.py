from random import randint

from django.db import models

from apps.auth_api.models import User
from apps.common.twilio import twilio


class PassRequest(models.Model):
    user = models.ForeignKey(User, null=True)
    number = models.CharField(max_length=100, null=True)
    code = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '{} <-> {}'.format(self.number, self.code)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = randint(1000, 9999)

            twilio.messages.create(
                to=self.number,
                from_='Mapala',
                body='Hello from Mapala! Your code: %s' % self.code
            )

        super().save(*args, **kwargs)
