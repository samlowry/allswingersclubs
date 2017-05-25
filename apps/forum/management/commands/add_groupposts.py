# -*- coding: utf-8 -*-

import random
import logging
import MySQLdb
from MySQLdb.cursors import DictCursor

from django.core.management.base import BaseCommand, CommandError

from directory.models import PostAuthor, ClubPost, ClubPostComment, UserBlogPost, UserBlogPostComment


class Command(BaseCommand):
    args = '<SITE_ID MIN_RECORDS MAX_RECORDS>'
    help = 'Add random number of posts to specific site'

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

    def _post_user_posts(self, site_id, min_rec, max_rec):
        posts_num = random.randint(min_rec, max_rec)
        self.logger.debug('Making {} users posts'.format(posts_num))

    def _post_club_posts(self, site_id, min_rec, max_rec):
        posts_num = random.randint(min_rec, max_rec)
        self.logger.debug('Making {} posts ot each group'.format(posts_num))

    def run(self, site_id, min_rec, max_rec):
        self.logger.info('Command "add_groupposts" executing with args:', site_id, min_rec, max_rec)

        self._post_user_posts(site_id, min_rec, max_rec)
        self._post_club_posts(site_id, min_rec, max_rec)

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
