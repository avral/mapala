import pprint
import logging
from multiprocessing import Pool

from redislite import Redis
from piston.steem import Steem
from piston.blockchain import Blockchain
from django.core.management.base import BaseCommand
from django.db.utils import InterfaceError
from django import db

from backend import settings
from apps.blockchains.sync import BaseUpdater

logger = logging.getLogger('mapala.fetch')

pool = Pool(processes=4)
redis = Redis('redis.db')


def get_block(steem, blockchain_name):
    last_block = redis.get('%s_last_block' % blockchain_name)

    if last_block is None:
        # Fitst app fetch
        last_block = Blockchain(steem).get_current_block_num()
        print(last_block, settings.LOCALE)

    return int(last_block)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('bc', nargs='?', type=str)
        parser.add_argument('block_num', nargs='?', type=int)

    def handle(self, *args, **options):
        settings.LOCALE = {
            'golos': 'ru', 'steemit': 'en'
        }[options['bc']]

        updater = BaseUpdater()
        steem = Steem(updater.blockchain.wss)

        last_block = options['block_num'] or get_block(steem, options['bc'])

        logger.info('Parse from %s block' % last_block)

        types = {
            'vote': updater.vote,
            'comment': updater.comment,
        }

        for op in Blockchain(
            steem,
            mode="irreversible"
        ).stream(['vote', 'comment'], start=last_block):
            to_do = types.get(op['type'])

            try:
                # TODO запилить асинихронность
                # pool.apply_async(to_do, [op])

                to_do(op)
            except InterfaceError:
                # При 2х одновременно запущенных блокчейнах
                # TODO Сделать одним прощессом все блокчейны
                db.connection.close()
                to_do(op)
            except KeyboardInterrupt:
                break
            except:
                logger.exception('Update err: %s' % pprint.pformat(op))

            block_num = int(op['block_num'])

            if last_block < block_num:
                last_block = block_num
                redis.set('%s_last_block' % options['bc'], last_block)
