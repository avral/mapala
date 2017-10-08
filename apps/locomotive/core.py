import logging

from pistonbase import operations
from piston.transactionbuilder import TransactionBuilder


from apps.locomotive.models import LocoMember


logger = logging.getLogger('mapala.fetch')


def locomotive_upvote(vote):
    from apps.blockchains.sync import BaseUpdater
    updater = BaseUpdater()

    members = LocoMember.objects.filter(
        user_blockchain__blockchain=updater.blockchain
    )

    done = 0
    for member in members.all():
        op = operations.Vote(
            **{"voter": member.user_blockchain.username,
               "author": vote['author'],
               "permlink": vote['permlink'],
               "weight": vote['weight']}
        )

        try:
            tx = TransactionBuilder(steem_instance=updater.rpc)
            tx.appendOps(op)
            tx.appendWif(member.wif)
            tx.sign()
            tx.broadcast()

            done += 1
        except Exception as e:
            logger.exception('Err upvote')

    # На случай если будут траблы с коннекшенами
    # from django.db import close_old_connections
    # close_old_connections()
    logger.info('Upvote {}, done: {}'.format(vote['permlink'], done))
