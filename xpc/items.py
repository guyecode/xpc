# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import json
import scrapy


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field(serializer=int)
    title = scrapy.Field()
    category = scrapy.Field()
    created_at = scrapy.Field()
    play_count = scrapy.Field(serializer=int)
    like_count = scrapy.Field(serializer=int)
    description = scrapy.Field()
    composers = scrapy.Field()
    comments = scrapy.Field()