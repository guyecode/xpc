# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import json
import scrapy
from scrapy import Field


class PostItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    pid = Field()
    title = Field()
    thumbnail = Field()
    preview = Field()
    video = Field()
    video_format = Field()
    duration = Field()
    category = Field()
    created_at = Field()
    play_counts = Field()
    like_counts = Field()
    description = Field()


class ComposerItem(scrapy.Item):
    cid = Field()
    banner = Field()
    avatar = Field()
    verified = Field()
    name = Field()
    intro = Field()
    like_counts = Field()
    fans_counts = Field()
    follow_counts = Field()
    location = Field()
    career = Field()

class CommentItem(scrapy.Item):
    commentid = Field()
    pid = Field()
    cid = Field()
    avatar = Field()
    uname = Field()
    created_at = Field()
    content = Field()
    like_counts = Field()
    reply = Field()


class CopyrightItem(scrapy.Item):
    pcid = Field()
    pid = Field()
    cid = Field()
    roles = Field()