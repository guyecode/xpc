# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pickle
import pymysql


class MysqlPipeline(object):

    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            db='xpc_1811',
            charset='utf8mb4'
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # 通过反向zip，将item中的key和value分开，并保持一一对应的顺序
        cols, values = zip(*item.items())
        # 组装SQL语句
        sql = "INSERT INTO `{}` ({}) VALUES " \
              "({}) ON DUPLICATE KEY UPDATE {}".format(
            item.table_name,
            # 将列名以逗号隔开
            ','.join(['`%s`' % col for col in cols]),
            # 组装N个%s占位符，N等于values的长度
            ','.join(['%s'] * len(values)),
            # 组装若干个键值对，`rank`='32',`name`='圣路易斯华盛顿大学',`country`='美国'
            ','.join(['`{}`=%s'.format(col) for col in cols])
        )
        # 因为on duplicate语法后面也要跟%s，
        # 所以占位符的数量增加了一倍，那values也要乘以2
        self.cur.execute(sql, values * 2)
        # 打印上一次执行的SQL语句
        # print(self.cur._last_executed)
        self.conn.commit()

        return item
