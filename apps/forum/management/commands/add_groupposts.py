# -*- coding: utf-8 -*-

import random
import logging
import MySQLdb
from django.contrib.sites.models import Site
from datetime import datetime, timedelta
from dateutil.parser import parse as date_parse
from MySQLdb.cursors import DictCursor

from django.core.management.base import BaseCommand, CommandError

from forum.models import PostAuthor, Group, GroupPost


class Command(BaseCommand):
    args = '<SITE_ID MIN_RECORDS MAX_RECORDS>'
    help = 'Add random number of posts to specific site'

    SITE_TO_GROUP_CATEGORY = {
        1: 2,
        2: 4,
        3: 3,
        4: 1,
    }

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.logger = self._init_logger('add_groupposts')

        try:
            self.source_db = MySQLdb.connect(
                host="localhost",
                user="fetlife",
                passwd="fetlife",
                db="fetlife",
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
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formater)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
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
            obj = model.objects.get(**search_fields)
        except model.DoesNotExist:
            obj = model(**fields)
            obj.save()
            created = True

        return obj, created

    def _post_user_posts(self, site_id, min_rec, max_rec):
        posts_num = random.randint(min_rec, max_rec)
        self.logger.debug('Making {} users posts'.format(posts_num))

    def _post_group_posts(self, site_id, min_rec, max_rec):
        posts_num = random.randint(min_rec, max_rec)
        self.logger.debug('Making {} posts ot each group'.format(posts_num))

        category = self.SITE_TO_GROUP_CATEGORY.get(site_id)

        if not category:
            self.logger.error('Unable to find mapping of site {} to category'.format(site_id))
            return

        cursor = self.source_db.cursor()
        site = Site.objects.get(pk=site_id)

        sql = """
            SELECT
                p.topic_id AS topic_id,
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
                -- AND p.unprocessable <> 1
            ORDER BY time
            LIMIT {posts_num};
        """.format(category=category, posts_num=posts_num)

        cursor.execute(sql)

        for row in cursor.fetchall():
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

                author, _ = self._get_or_create(PostAuthor, dict(
                    orig_user_id=row['user_id'],
                    name=row['user_name'].strip()
                ), dict(
                    orig_user_id=row['user_id']
                ))

                post = GroupPost(
                    group=group,
                    author=author,
                    orig_post_id=row['topic_id'],
                    title=row['topic_title'].strip(),
                    content=row['topic_text'].strip(),
                    created_at=self.fix_date(post_date_time)
                )

                post.save()
            except Exception as ex:
                self.logger.exception(ex)

            sql = 'UPDATE group_posts SET processed=1 WHERE topic_id={}'.format(row['topic_id'])
            cursor.execute(sql)
            self.source_db.commit()

    def run(self, site_id, min_rec, max_rec):
        self.logger.info('Command "add_groupposts" executing with args: {} {} {}'.format(site_id, min_rec, max_rec))

        # self._post_user_posts(site_id, min_rec, max_rec)
        self._post_group_posts(site_id, min_rec, max_rec)

        self.logger.info('Command "add_groupposts" finished')

    def handle(self, *args, **options):
        site_id, min_rec, max_rec = (args + (None,) * 3)[:3]

        if not site_id:
            raise CommandError('Option SITE_ID is required')

        if not min_rec:
            raise CommandError('Option MIN_REC is required')

        if not max_rec:
            raise CommandError('Option MAX_REC is required')

        site_id = int(site_id)
        min_rec = int(min_rec)
        max_rec = int(max_rec)

        self.run(site_id, min_rec, max_rec)
