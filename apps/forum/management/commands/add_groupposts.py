# -*- coding: utf-8 -*-

import os
import random
import logging
import MySQLdb
from datetime import datetime
from django.contrib.sites.models import Site
from datetime import datetime, timedelta
from dateutil.parser import parse as date_parse
from MySQLdb.cursors import DictCursor

from django.core.management.base import BaseCommand, CommandError

from forum.models import PostAuthor, Group, GroupPost, GroupPostComment
from forum.random_names import get_random_name


class Command(BaseCommand):
    args = '<SITE_ID MIN_RECORDS MAX_RECORDS [LOG_LEVEL]>'
    help = 'Add random number of posts to specific site'

    SITE_TO_GROUP_CATEGORY = {
        1: 2,
        2: 4,
        3: 3,
        4: 1,
    }

    LOG_LEVEL = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING
    }

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.logger = self._init_logger('add_groupposts')

        try:
            self.source_db = MySQLdb.connect(
                #host="localhost",
                #user="fetlife",
                #passwd="fetlife",
                #db="fetlife",
                #cursorclass=DictCursor
                host=os.getenv('DATABASE_HOST', '138.197.211.96'),
                user=os.getenv('DATABASE_USER', 'fetlife-79d0d24e487711e7a919'),
                passwd=os.getenv('DATABASE_PASSWORD', '_Wyhr6*?6aJYAqtNb9w2qM+F96UaEE'),
                db=os.getenv('DATABASE_DBNAME', 'fetlife'),
                cursorclass=DictCursor
            )
        except MySQLdb.Error as ex:
            self.logger.exception(ex)
            raise

    def _init_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        formater = logging.Formatter('%(asctime)s | %(levelname)7s | %(funcName)s:%(lineno)4s | %(message)s')

        file_handler = logging.FileHandler('/var/log/add_groupposts.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formater)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formater)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def fix_date(self, dt, src_dt=None):
        now = datetime.now()
        result_date = datetime(now.year, now.month, now.day, dt.hour, dt.minute, dt.second)

        if result_date > now:
            result_date += timedelta(days=1)

        if src_dt:
            days_distance = (dt - src_dt)
            if days_distance.days > 0:
                result_date += days_distance

        return result_date

    def _get_or_create(self, model, fields, search_fields):
        created = False

        try:
            manager = getattr(model, 'objects', None)

            if not manager:
                manager = getattr(model, 'current_site_only', None)

            if not manager:
                raise AttributeError('Unable to find object manager for model %s' % model)

            obj = manager.get(**search_fields)
        except model.DoesNotExist:
            obj = model(**fields)
            obj.save()
            created = True

        return obj, created

    def _post_user_posts(self, site_id, min_rec, max_rec):
        posts_num = random.randint(min_rec, max_rec)
        self.logger.debug('Making {posts_num} users posts'.format(posts_num=posts_num))

    def _post_group_posts(self, site_id, min_rec, max_rec):
        posts_num = random.randint(min_rec, max_rec)
        self.logger.debug('Posting {posts_num} posts to each group'.format(posts_num=posts_num))

        category = self.SITE_TO_GROUP_CATEGORY.get(site_id)

        if not category:
            self.logger.error('Unable to find mapping of site {site_id} to category'.format(site_id=site_id))
            return

        posts_cursor = self.source_db.cursor()
        comments_cursor = self.source_db.cursor()
        site = Site.objects.get(pk=site_id)

        sql = """
            SELECT
                p.topic_id AS topic_id,
                p.src_group_post_id AS src_topic_id,
                p.title AS topic_title,
                p.post_text as topic_text,
                p.time as topic_time,

                u.user_id AS user_id,
                u.fake_nickname AS user_name,

                g.group_id AS group_id,
                g.group_name AS group_name,
                g.description AS group_description
            FROM group_posts p
            LEFT JOIN groups g ON p.group_id=g.group_id
            LEFT JOIN users u ON p.author_id=u.user_id
            WHERE
                p.time IS NOT NULL
                AND p.processed IS NULL
                AND g.group_id IS NOT NULL
                AND u.fake_nickname IS NOT NULL
                AND g.category_id={category}
                AND NOT (p.unprocessable IS NOT NULL AND p.unprocessable <> 1)
            ORDER BY time
            LIMIT {posts_num};
        """.format(category=category, posts_num=posts_num)

        self.logger.debug('Posts SQL execution started')
        posts_cursor.execute(sql)
        self.logger.debug('Posts SQL execution finished')

        for row in posts_cursor.fetchall():
            try:
                post_date_time = date_parse(row['topic_time'].strip())

                group, _ = self._get_or_create(Group, dict(
                    site=site,
                    orig_group_id=row['group_id'],
                    name=row['group_name'].strip(),
                    description=row['group_description'].strip()
                ), dict(
                    orig_group_id=row['group_id']
                ))

                self.logger.debug('Group {orig_group_id} {cor} '.format(
                    orig_group_id=group.orig_group_id, cor='retrieved' if _ else 'created'
                ))

                author, _ = self._get_or_create(PostAuthor, dict(
                    orig_user_id=row['user_id'],
                    name=row['user_name'].strip()
                ), dict(
                    orig_user_id=row['user_id']
                ))

                self.logger.debug('Author {orig_user_id} {cor}'.format(
                    orig_user_id=author.orig_user_id, cor='retrieved' if _ else 'created'
                ))

                post = GroupPost(
                    group=group,
                    author=author,
                    orig_post_id=row['topic_id'],
                    title=row['topic_title'].strip(),
                    content=row['topic_text'].strip(),
                    created_at=self.fix_date(post_date_time)
                )

                self.logger.info('Created post with original id {orig_post_id} in group id {orig_group_id}'.format(
                    orig_post_id=post.orig_post_id, orig_group_id=row['group_id']
                ))
                post.save()

                sql = """
                    SELECT
                        c.topic_comment_id AS comment_id,
                        c.comment_text AS comment_text,
                        c.time AS comment_date_time,

                        u.user_id AS user_id,
                        u.fake_nickname AS user_name
                    FROM group_posts_comments c
                    LEFT JOIN users u ON c.src_commenter_id=u.src_user_id
                    WHERE
                        c.src_topic_id={src_topic_id} OR c.topic_id={topic_id};
                """.format(src_topic_id=row['src_topic_id'], topic_id=row['topic_id'])

                self.logger.debug('>> Comments SQL execution started')
                comments_cursor.execute(sql)
                self.logger.debug('>> Comments SQL execution finished')

                for comm in comments_cursor.fetchall():
                    comment_author, _ = self._get_or_create(PostAuthor, dict(
                        orig_user_id=comm['user_id'],
                        name=comm['user_name'] or get_random_name()
                    ), dict(
                        orig_user_id=comm['user_id']
                    ))

                    self.logger.debug('Comment author {orig_user_id} {cor}'.format(
                        orig_user_id=comment_author.orig_user_id, cor='retrieved' if _ else 'created'
                    ))

                    comment_date_time = date_parse(comm['comment_date_time'].strip())

                    comment = GroupPostComment(
                        group_post=post,
                        author=comment_author,
                        content=comm['comment_text'],
                        created_at=self.fix_date(comment_date_time)
                    )
                    comment.save()

                    self.logger.debug('Comment to post {orig_post_id} created'.format(orig_post_id=post.orig_post_id))
            except Exception as ex:
                self.logger.exception(ex)

            sql = 'UPDATE group_posts SET processed=1 WHERE topic_id={topic_id}'.format(topic_id=row['topic_id'])
            posts_cursor.execute(sql)
            self.source_db.commit()

    def run(self, site_id, min_rec, max_rec, log_level=None):
        if log_level and log_level.lower() in self.LOG_LEVEL:
            self.logger.setLevel(self.LOG_LEVEL[log_level.lower()])

        self.logger.info('Command "add_groupposts" executing with args: {site_id} {min_rec} {max_rec}'.format(
            site_id=site_id, min_rec=min_rec, max_rec=max_rec
        ))

        # self._post_user_posts(site_id, min_rec, max_rec)
        self._post_group_posts(site_id, min_rec, max_rec)

        self.logger.info('Command "add_groupposts" finished')

    def handle(self, *args, **options):
        site_id, min_rec, max_rec, log_level = (args + (None,) * 4)[:4]

        if not site_id:
            raise CommandError('Option SITE_ID is required')

        if not min_rec:
            raise CommandError('Option MIN_REC is required')

        if not max_rec:
            raise CommandError('Option MAX_REC is required')

        site_id = int(site_id)
        min_rec = int(min_rec)
        max_rec = int(max_rec)

        self.run(site_id, min_rec, max_rec, log_level)
