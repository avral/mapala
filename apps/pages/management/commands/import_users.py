import json
import logging

from django.db.models import Q
from django.core.management.base import BaseCommand

from apps.auth_api.models import BlockChain, UserBlockChain, User


golos_bc = BlockChain.objects.get(name='golos')
steemit_bc = BlockChain.objects.get(name='steemit')


class Command(BaseCommand):
    def handle(self, *args, **options):
        # чистим всех юзеров кроме админа
        input('Вся база будет очищена!!')
        User.objects.filter(~Q(username='admin')).delete()

        with open('./apps/pages/management/commands/dump.json') as data_file:
            data = json.load(data_file)

        for user in data['user']:
            username = user['username']
            email = user['email']

            steemit = user.get('steem')
            golos = user.get('golos')

            users_bc = UserBlockChain.objects.filter(
                Q(blockchain=golos_bc, username=golos) |
                Q(blockchain=steemit_bc, username=steemit)
            )

            if users_bc.exists():
                exists_user = users_bc.first().user

                exists_user_ico = [i for i in data['ico'] if i['name'] == exists_user.username]
                user_ico = [i for i in data['ico'] if i['name'] == username]

                if exists_user_ico and user_ico:
                    logging.warning('Токены есть в обоих аккаунтах! %s - %s' % (
                        exists_user.username, username
                    ))
                    continue

                if user_ico and not exists_user_ico:
                    new_name = user_ico[0]['name']
                    new_user = next(u for u in data['user'] if u['username'] == new_name)

                    exists_user.username = new_user['username']
                    exists_user.password_hash = new_user['password_hash']
                    exists_user.btc_wallet = new_user['btc_wallet']
                    exists_user.btc_wallet_direct = new_user['btc_wallet_direct']

                    exists_user.save()

                continue

            user_for_create = {
                'username': username,
                'password': 'bcrypt_sha256$%s' % user['password_hash'],
                'btc_wallet': user['btc_wallet'],
                'btc_wallet_direct': user['btc_wallet_direct']
            }

            if len(username.strip()) < 1:
                continue

            if User.objects.filter(username=username).exists():
                continue

            if not User.objects.filter(email=email).exists():
                user_for_create['email'] = email

            user = User.objects.create(**user_for_create)

            if steemit != 'NULL':
                UserBlockChain.objects.create(
                    blockchain=steemit_bc,
                    username=steemit,
                    user=user
                )

            if golos != 'NULL':
                UserBlockChain.objects.create(
                    blockchain=golos_bc,
                    username=golos,
                    user=user
                )

        self.stdout.write(
            self.style.SUCCESS('DONE: Users - %s' % User.objects.count())
        )
