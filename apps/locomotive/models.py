from django.db import models

from apps.auth_api.models import UserBlockChain


class LocoMember(models.Model):
    """ Ключик для участия в паравозике """
    user_blockchain = models.ForeignKey(UserBlockChain, null=True)
    wif = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.user_blockchain.username
