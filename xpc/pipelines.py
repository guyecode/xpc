# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pprint
import traceback
from pymysql.cursors import DictCursor
from pymysql import OperationalError
from pymysql.constants.CR import CR_SERVER_GONE_ERROR,  CR_SERVER_LOST, CR_CONNECTION_ERROR
from twisted.internet import defer
from twisted.enterprise import adbapi

from xpc.items import PostItem, ComposerItem, CommentItem, CopyrightItem

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class MySQLPipeline(object):  #
    """
    Defaults:
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = None
    MYSQL_PASSWORD = ''
    MYSQL_DB = None
    MYSQL_TABLE = None
    MYSQL_UPSERT = False
    MYSQL_RETRIES = 3
    MYSQL_CLOSE_ON_ERROR = True
    Pipeline:
    ITEM_PIPELINES = {
       'scrapy_mysql_pipeline.MySQLPipeline': 300,
    }
    """
    stats_name = 'mysql_pipeline'
    table_name = ''
    item_class = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.stats = crawler.stats
        self.settings = crawler.settings
        db_args = {
            'host': self.settings.get('MYSQL_HOST', 'localhost'),
            'port': self.settings.get('MYSQL_PORT', 3306),
            'user': self.settings.get('MYSQL_USER', None),
            'password': self.settings.get('MYSQL_PASSWORD', ''),
            'db': self.settings.get('MYSQL_DB', None),
            'charset': 'utf8mb4',
            'cursorclass': DictCursor,
            'cp_reconnect': True,
        }
        self.retries = self.settings.get('MYSQL_RETRIES', 1)
        self.close_on_error = self.settings.get('MYSQL_CLOSE_ON_ERROR', True)
        self.upsert = self.settings.get('MYSQL_UPSERT', False)
        self.table = self.table_name or self.settings.get('MYSQL_TABLE', None)
        self.db = adbapi.ConnectionPool('pymysql', **db_args)

    def close_spider(self, spider):
        self.db.close()

    # @defer.inlineCallbacks
    def process_item(self, item, spider):
        # logger.info(item)
        if isinstance(item, self.item_class):
            retries = self.retries
            status = False
            while retries:
                try:

                    self.db.runInteraction(self._process_item, item)
                except OperationalError as e:
                    if e.args[0] in (
                            CR_SERVER_GONE_ERROR,
                            CR_SERVER_LOST,
                            CR_CONNECTION_ERROR,
                    ):
                        retries -= 1
                        logger.info('%s %s attempts to reconnect left', e, retries)
                        self.stats.inc_value('{}/reconnects'.format(self.stats_name))
                        continue
                    logger.exception('%s', pprint.pformat(item))
                    self.stats.inc_value('{}/errors'.format(self.stats_name))
                except Exception:
                    logger.info(item)
                    logger.exception('%s', pprint.pformat(item))
                    self.stats.inc_value('{}/errors'.format(self.stats_name))
                else:
                    status = True  # executed without errors
                break
            else:
                if self.close_on_error:  # Close spider if connection error happened and MYSQL_CLOSE_ON_ERROR = True
                    spider.crawler.engine.close_spider(spider, '{}_fatal_error'.format(self.stats_name))
        return item

    def _generate_sql(self, data):
        columns = lambda d: ', '.join(['`{}`'.format(k) for k in d])
        values = lambda d: [v for v in d.values()]
        placeholders = lambda d: ', '.join(['%s'] * len(d))
        if self.upsert:
            sql_template = 'INSERT INTO `{}` ( {} ) VALUES ( {} ) ON DUPLICATE KEY UPDATE {}'
            on_duplicate_placeholders = lambda d: ', '.join(['`{}` = %s'.format(k) for k in d])
            return (
                sql_template.format(
                    self.table, columns(data),
                    placeholders(data), on_duplicate_placeholders(data)
                ),
                values(data) + values(data)
            )
        else:
            sql_template = 'INSERT INTO `{}` ( {} ) VALUES ( {} )'
            return (
                sql_template.format(self.table, columns(data), placeholders(data)),
                values(data)
            )

    def _process_item(self, interaction, item):
        sql, data = self._generate_sql(item)
        try:
            interaction.execute(sql, data)
        except Exception:
            traceback.print_exc()
            logger.warn(sql)
            logger.warn(data)
        self.stats.inc_value('{}/saved'.format(self.stats_name))


class PostPipeline(MySQLPipeline):
    stats_name = 'post_pipeline'
    table_name = 'posts'
    item_class = PostItem


class ComposerPipeline(MySQLPipeline):
    stats_name = 'composer_pipline'
    table_name = 'composers'
    item_class = ComposerItem


class CommentPipeline(MySQLPipeline):
    stats_name = 'comment_pipline'
    table_name = 'comments'
    item_class = CommentItem


class CopyrightItemPipeline(MySQLPipeline):
    stats_name = 'copyright_pipline'
    table_name = 'copyrights'
    item_class = CopyrightItem