import logging

from django.core.management.base import BaseCommand

from apps.blockchains.sync import BaseUpdater

logger = logging.getLogger('mapala.fetch_all')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('bc', nargs='?', type=str)

    def handle(self, *args, **options):
        updater = BaseUpdater(options['bc'], db_connect=True)

        # Посты
        i = 0
        for post in updater.db.get_all_posts():
            try:
                updater.upgrade_post(post)
                i += 1
            except:
                logger.exception('Ошибка в загрузке поста')
        print(i, 'постов загруженно')

        i = 0
        for comm in updater.db.get_all_comments():
            try:
                r = updater.upgrade_comment(comm)

                if r is not None:
                    i += 1
            except:
                logger.exception('Ошибка в загрузке коммента')
        print(i, 'комментов загруженно')
