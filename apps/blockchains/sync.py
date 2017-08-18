import logging
import pprint

from piston.steem import Steem
from piston.post import Post
from piston.exceptions import PostDoesNotExist

from django.contrib.gis.geos import Point
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from backend.settings import APP_FETCH_FROM
from apps.auth_api.models import UserBlockChain, BlockChain, User
from apps.pages.models import Page, Comment
from apps.blockchains.data_bases import BlockChainDB


logger = logging.getLogger('mapala.fetch')


class BaseUpdater:
    """ Class for update objects in Mpala database """
    def __init__(self, db_connect=False):
        self.blockchain = BlockChain.current()
        self.db = BlockChainDB() if db_connect else None
        self.rpc = Steem(self.blockchain.wss)

    def comment(self, comment):
        """ Update or create comment """
        post = Post(comment, steem_instance=self.rpc)

        try:
            if post.is_comment():
                self.upgrade_comment(post)
            else:
                if post.parent_permlink == APP_FETCH_FROM:
                    created_post = self.upgrade_post(post)
                    if created_post is not None:
                        # Временно, для выявления магии скорейскими постами
                        if self.blockchain.name == 'steemit':
                            logger.info('Созданный пост %s' % pprint.pformat(comment))
        except PostDoesNotExist:
            pass

    def vote(self, vote):
        if (Page.on_bc.filter(permlink=vote['permlink']).exists() and
                UserBlockChain.on_bc.filter(username=vote['author'])):
            # Обновляем каждый пост по которому кто то голосует
            self.update_post(vote['author'], vote['permlink'])

    def upgrade_comment(self, comm):
        author = self.get_author(comm.parent_author)
        page = None

        if Page.objects.filter(
            permlink=comm.parent_permlink,
            author=author
        ).exists():
            page = Page.objects.get(
                permlink=comm.parent_permlink,
                author=author,
            )
        else:
            parent_comm = Comment.objects.filter(
                permlink=comm.parent_permlink,
                author=author,
            ).first()

        if page is not None:
            comment = self.get_comment_ins(comm, page, parent=None)
        else:
            if parent_comm is None:
                return None

            comment = self.get_comment_ins(
                comm,
                parent_comm.page,
                parent=parent_comm
            )

        comment.save()

    def aware(self, date):
        return timezone.make_aware(date, timezone.get_current_timezone())

    def fetch(self, last_update=None):
        self.posts, self.count = self.db.get_posts_with_comments(last_update)

        return self.count

    def fetch_post(self, permlink):
        self.posts = self.db.get_post_by_permlink(permlink)

    def update_post(self, author, permlink):
        """ Обновляет пост по автору и пермлинку """
        # Временно, для выявления магии скорейскими постами
        if self.blockchain.name == 'steemit':
            logger.info('Update post: %s %s' % (author, permlink))

        post = self.rpc.get_content({
            'permlink': permlink,
            'author': author
        })

        return self.upgrade_post(post)

    def upgrade_post(self, p):
        """ Обновляет пост в соответствии с принимаемым Post() """
        payout = float(p.total_payout_value)
        pending_payout = float(p.total_pending_payout_value)

        author = self.get_author(p.author)

        post = {'permlink': p.permlink,
                'author': self.get_author(p.author),
                'defaults': {
                    'title': p.title,
                    'updated_at': self.aware(p.last_update),
                    'created_at': self.aware(p.created),
                    'author': author,
                    'permlink': p.permlink,
                    'body': p.body,
                    'meta': p.meta,
                    'total_payout_value': payout,
                    'total_pending_payout_value': pending_payout,
                    'blockchain': self.blockchain,
                }}

        if coord_exists(p.meta):
            position_text, lat, lng = get_position(p.meta)

            post['defaults']['position_text'] = position_text
            post['defaults']['position'] = Point(lng, lat)
            post['defaults']['has_point'] = True
        else:
            post['defaults']['has_point'] = False

        post, _ = Page.objects.update_or_create(**post)

        return post

    def upgrade_comments(self, post_ins, items):
        def make_tree(ins):
            nodes = [
                self.get_comment_ins(i, post_ins, parent=ins)
                for i in items if i.parent_permlink == ins.permlink
            ]

            return [make_tree(ins) for ins in nodes]

        post_permlink = post_ins.permlink

        root_ns = [n for n in items if n.parent_permlink == post_permlink]

        for root in root_ns:
            make_tree(
                self.get_comment_ins(root, post_ins, parent=None)
            )

    def upgrade(self):
        created_posts = []
        i = 0
        for items in self.posts:
            try:
                # В каждой итерации запрос к базе
                post_data = next(
                    p for p in items if p.parent_permlink == APP_FETCH_FROM)
                try:
                    post_ins = self.upgrade_post(post_data)
                    created_posts.append(post_ins)
                except:
                    logging.exception('Ошибка апгрейда поста', post_data.permlink)

                    continue

                try:
                    self.upgrade_comments(post_ins, items)
                except:
                    logging.exception(
                        'Ошибка загрузки комментариев',
                        post_data.permlink
                    )

                i += 1
                print(i, '/', self.count)
            except Exception as e:
                logging.exception('Ошибка выборки поста')

        return created_posts

    def get_comment_ins(self, data, post, **kwargs):
        comm = {
            'page': post,
            'updated_at': self.aware(data.last_update),
            'created_at': self.aware(data.created),
            'body': data.body
        }

        comm.update(**kwargs)

        return Comment.objects.update_or_create(
            permlink=data.permlink,
            author=self.get_author(data.author),
            defaults=comm
        )[0]

    def get_author(self, username):
        try:
            user_bc = UserBlockChain.objects.get(
                username=username.lower(),
                blockchain=self.blockchain
            )
        except ObjectDoesNotExist:
            user, _ = User.objects.get_or_create(
                username='{}_unactivated_{}'.format(username,
                                                    self.blockchain.name))

            UserBlockChain.objects.create(
                username=username,
                blockchain=self.blockchain,
                user=user
            )

            return user

        return user_bc.user


def coord_exists(meta):
    if 'location' not in meta:
        return False

    if 'coordinates' in meta and len(meta['coordinates'].split(',')) == 2:
        return True

    location = meta['location']

    if 'lat' in location and 'lng' in location:
        return True

    return False


def get_position(meta):
    if 'coordinates' in meta:
        # Старая структура локации
        name = meta['location']
        lat, lng = meta['coordinates'].split(',')
    else:
        name = meta['location']['name']
        lat, lng = meta['location']['lat'], meta['location']['lng']

    return name, float(lat), float(lng)
