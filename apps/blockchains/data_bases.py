import logging
import json
import pyodbc
from collections import namedtuple


from backend.settings import (
    BLOCKCHAIN_DATABASES,
    APP_FETCH_FROM
)


Post = namedtuple('Post', [
    'title',
    'author',
    'permlink',
    'parent_permlink',
    'body',
    'meta',
    'created',
    'last_update',
    'last_payout',
    'total_pending_payout_value',
    'total_payout_value',
    ]
)

Comment = namedtuple('Comment', [
    'author',
    'permlink',
    'parent_author',
    'parent_permlink',
    'body',
    'created',
    'last_update',
    ]
)


class BlockChainDB:
    # DOCS https://docs.microsoft.com/en-us/azure/sql-database/sql-database-connect-query-python
    params_tpl = 'DRIVER={};SERVER={};PORT=1443;DATABASE={};UID={};PWD={}'

    def __init__(self, blockchain):
        self.blockchain = blockchain

        db_params = BLOCKCHAIN_DATABASES[blockchain]
        self.conn = pyodbc.connect(
            self.params_tpl.format(
                db_params['driver'],
                db_params['server'],
                db_params['database'],
                db_params['username'],
                db_params['password']
            ), autocommit=True
        )
        self.cursor = self.conn.cursor()

    def exec(self, query):
        try:
            self.cursor.execute(query)
        except pyodbc.Error:
            logging.exception('Err sql execute')
            return self.exec(query)

        return self.cursor

    def get_all_comments(self):
        query = """
        SELECT
            author, permlink, parent_author, parent_permlink, body,
            created, last_update
        FROM
            Comments
        WHERE
            permlink <> 'test' AND depth > 0
        ORDER BY
            created ASC
        """
        cursor = self.conn.cursor()
        cursor.execute(query)

        return [Comment(
            author=row[0],
            permlink=row[1],
            parent_author=row[2],
            parent_permlink=row[3],
            body=row[4],
            created=row[5],
            last_update=row[6]) for row in cursor]

    def get_all_posts(self):
        query = """
        SELECT
            title, author, permlink, parent_permlink, body,
            json_metadata, created, last_update, last_payout,
            total_payout_value, total_pending_payout_value
        FROM
            Comments
        WHERE
            parent_author = '' AND parent_permlink = '%s'
            AND permlink <> 'test'
        ORDER BY
            created ASC
        """ % APP_FETCH_FROM
        cursor = self.conn.cursor()
        cursor.execute(query)

        return [Post(
            title=row[0],
            author=row[1],
            permlink=row[2],
            parent_permlink=row[3],
            body=row[4],
            meta=self._json_meta_load(row[5]),
            created=row[6],
            last_update=row[7],
            last_payout=row[8],
            total_payout_value=row[9],
            total_pending_payout_value=row[10]) for row in cursor]

    def get_user_by_posting_key(self, key):
        query = """
            SELECT
                name
            FROM
                Accounts
            WHERE
                posting LIKE '%{}%'
            """.format(key)

        try:
            return next(self.exec(query))[0]
        except StopIteration:
            return None

    def get_posts_with_comments(self, last_update=None):
        """
        Возвращает количество постои и генератор для вытягивания постов
        по одному запросу со всеми комментариями к нему
        """

        posts_sql = """
        SELECT FIRST_VALUE(Id) OVER(PARTITION BY author, permlink ORDER BY last_update DESC)
        FROM Comments
        WHERE
            parent_author = '' AND parent_permlink = '%s' AND (
                (
                    JSON_VALUE(json_metadata, '$.location') <> '' AND
                    JSON_VALUE(json_metadata, '$.coordinates') <> ''
                ) OR (
                    JSON_VALUE(json_metadata, '$.location.name') <> ''
                )
            ) AND permlink <> 'test'
        """ % APP_FETCH_FROM

        if last_update is not None:
            posts_sql += " AND created > '%s'" % last_update

        postsCursor = self.conn.cursor()
        postsCursor.execute(posts_sql)

        posts = [p[0] for p in postsCursor]

        return self.posts_generator(posts), len(posts)

    def get_post_by_permlink(self, permlink):
        query = """
            WITH Recursive AS (
                SELECT
                title, author, permlink, parent_permlink, body,
                json_metadata, created, last_update, last_payout,
                total_payout_value, total_pending_payout_value
                FROM
                    Comments e with (updlock)
                WHERE
                    e.permlink = '%s'
                UNION ALL
                SELECT
                    e.title, e.author, e.permlink, e.parent_permlink,
                    e.body, e.json_metadata, e.created,
                    e.last_update, e.last_payout, e.total_payout_value,
                    e.total_pending_payout_value
                FROM Comments e
                    JOIN Recursive r ON e.parent_permlink = r.permlink
            )
            SELECT
                title, author, permlink, parent_permlink, body,
                json_metadata, created, last_update, last_payout,
                total_payout_value, total_pending_payout_value
            FROM Recursive r;
        """ % permlink

        cursor = self.conn.cursor()
        cursor.execute(query)
        yield [Post(
                    title=row[0],
                    author=row[1],
                    permlink=row[2],
                    parent_permlink=row[3],
                    body=row[4],
                    meta=self._json_meta_load(row[5]),
                    created=row[6],
                    last_update=row[7],
                    last_payout=row[8],
                    total_payout_value=row[9],
                    total_pending_payout_value=row[10]) for row in cursor]

    def posts_generator(self, posts):
        comments_sql = """
        WITH Recursive AS (
            SELECT
            title, author, permlink, parent_permlink, body,
            json_metadata, created, last_update, last_payout,
            total_payout_value, total_pending_payout_value
            FROM
                Comments e with (updlock)
            WHERE
                e.ID = {}
            UNION ALL
            SELECT
                e.title, e.author, e.permlink, e.parent_permlink,
                e.body, e.json_metadata, e.created,
                e.last_update, e.last_payout, e.total_payout_value,
                e.total_pending_payout_value
            FROM Comments e
                JOIN Recursive r ON e.parent_permlink = r.permlink
        )
        SELECT
            title, author, permlink, parent_permlink, body,
            json_metadata, created, last_update, last_payout,
            total_payout_value, total_pending_payout_value
        FROM Recursive r
        OPTION (MAXRECURSION 50);
        """
        for post in posts:
            try:
                cursor = self.conn.cursor()
                cursor.execute(comments_sql.format(post))

                yield [Post(
                    title=row[0],
                    author=row[1],
                    permlink=row[2],
                    parent_permlink=row[3],
                    body=row[4],
                    meta=self._json_meta_load(row[5]),
                    created=row[6],
                    last_update=row[7],
                    last_payout=row[8],
                    total_payout_value=row[9],
                    total_pending_payout_value=row[10]) for row in cursor]
            except:
                logging.exception('Ошибка выгрузки поста: %s' % post)

    def _json_meta_load(self, meta):
        if meta.strip() == '':
            return {}

        try:
            return json.loads(meta)
        except json.decoder.JSONDecodeError:
            logging.warn('Не валидный JSON в комментарии: %s' % meta)
            return {}
