import json

from django.db.models import Q
from django.core.management.base import BaseCommand

from apps.auth_api.models import BlockChain, UserBlockChain, User


golos_bc = BlockChain.objects.get(name='golos')
steemit_bc = BlockChain.objects.get(name='steemit')


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('./apps/pages/management/commands/dump.json') as data_file:
            data = json.load(data_file)

        for user in data['user']:
            if not User.objects.filter(username=user['username']).exists():
                user_for_create = {
                    'username': user['username'],
                    'password': 'bcrypt_sha256$%s' % user['password_hash'],
                    'btc_wallet': user['btc_wallet'],
                    'btc_wallet_direct': user['btc_wallet_direct']
                }

                user = User.objects.create(**user_for_create)
                print(user.username)
