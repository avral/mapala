import logging

from pistonbase import operations
from pistonapi.exceptions import AlreadyVotedSimilarily, OnlyVoteOnceEvery3Seconds
from piston.transactionbuilder import TransactionBuilder


from apps.common.utils import ScheduleArray
from apps.locomotive.models import LocoMember


logger = logging.getLogger('mapala.fetch')


def locomotive_upvote(vote):
    from apps.blockchains.sync import BaseUpdater
    updater = BaseUpdater()

    members = LocoMember.objects.filter(
        user_blockchain__blockchain=updater.blockchain
    )

    sch_queue = ScheduleArray((i, 0) for i in members.all())

    done = 0
    for member in sch_queue:
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
        except OnlyVoteOnceEvery3Seconds:
            # Добавляем обратно в список, на повтор через 3 сек
            sch_queue.append(member, 3)
        except AlreadyVotedSimilarily:
            pass
        except Exception as e:
            logger.exception('Err upvote')

    # На случай если будут траблы с коннекшенами
    # from django.db import close_old_connections
    # close_old_connections()
    logger.info('Upvote {}, done: {}'.format(vote['permlink'], done))
