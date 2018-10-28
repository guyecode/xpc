# -*- coding: utf-8 -*-

import re
import random
import json
import scrapy
from scrapy import Request
from xpc.items import PostItem, CommentItem, ComposerItem, CopyrightItem

strip = lambda x: x.strip() if x else ''


def convert_int(s):
    if s:
        return int(s.replace(',', ''))
    return 0


ci = convert_int
cookies = {
    'Authorization': 'D0A7850E249EC0AE6249EC4345249ECB535249EC7C4535999D64',
    # 'PHPSESSID': 'sfanedt9sk0mkdkr68fc995l26',
}


def gen_sessid():
    letters = [chr(i) for i in range(97, 97 + 26)] + [str(i) for i in range(10)]
    return ''.join(random.choices(letters, k=26))


class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com', 'openapi-vtom.vmovier.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/sort-like?from=tabArticle']

    def start_requests(self):
        for url in self.start_urls:
            print('---'*50)
            yield Request(url, dont_filter=True, cookies=cookies)

    def parse(self, response):
        if response.text.find('系统繁忙') != -1:
            print('系统繁忙' * 20)
        url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
        post_list = response.xpath('//ul[@class="video-list"]/li')
        # pid_list = response.xpath('//ul[@class="video-list"]/li/@data-articleid').extract()
        # thumbnail_list = response.xpath('//ul[@class="video-list"]/li/a/img/@src').extract()
        # for pid, thumbnail in zip(pid_list, thumbnail_list):
        for post in post_list:
            pid = post.xpath('./@data-articleid').get()
            request = Request(url % pid, callback=self.parse_post)
            request.meta['pid'] = pid
            # 缩略图是延迟加载，所以要取它的_src属性
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            # yield request
        pages = response.xpath('//div[@class="page"]/a/@href').extract()
        for page in pages:
            cookies['PHPSESSID'] = gen_sessid()
            yield response.follow(page, cookies=cookies)

    def parse_post(self, response):
        pid = response.meta['pid']
        post = PostItem()
        post['pid'] = pid
        post['thumbnail'] = response.meta['thumbnail']
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()
        cates = response.xpath(
            '//span[contains(@class, "cate")]/a/text()').extract()
        post['category'] = '-'.join([cate.strip() for cate in cates])
        post['created_at'] = response.xpath(
            '//span[contains(@class, "update-time")]/i/text()').get()
        post['play_counts'] = response.xpath(
            '//i[contains(@class, "play-counts")]/@data-curplaycounts').get()
        post['like_counts'] = response.xpath(
            '//span[contains(@class, "like-counts")]/@data-counts').get()
        post['description'] = strip(response.xpath(
            '//p[contains(@class, "desc")]/text()').get())
        # 通过正则解析javascript代码，提取关键的vid参数
        vid, = re.findall(r'vid: \"(\w+)\"\,', response.text)
        post_url = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource,resource_origin?'
        request = Request(post_url % vid, callback=self.parse_video)
        request.meta['post'] = post
        yield request
        # 请求评论接口
        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&ajax=0&page=1'
        request = Request(comment_url % pid, callback=self.parse_comment)
        yield request
        # 提取所有的作者信息
        composer_list = response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li')
        composer_url = 'http://www.xinpianchang.com/u%s?from=articleList'
        for composer in composer_list:
            cid = composer.xpath('./a/@data-userid').get()
            request = Request(composer_url % cid, callback=self.parse_composer)
            request.meta['cid'] = cid
            yield request
            # 保存作者和作品之间的对应关系
            cr = CopyrightItem()
            cr['pcid'] = '%s_%s' % (cid, pid)
            cr['cid'] = cid
            cr['pid'] = pid
            # 同一个作者在不同的作品里担任的角色是不一样的，在这里保存这个信息
            cr['roles'] = composer.xpath('.//span[contains(@class, "roles")]/text()').get()
            yield cr

    def parse_composer(self, response):
        composer = ComposerItem()
        composer['cid'] = response.meta['cid']
        banner = response.xpath('//div[@class="banner-wrap"]/@style').get()
        composer['banner'], = re.findall(r'background-image:url\((.+?)\)', banner)
        composer['avatar'] = response.xpath(
            '//span[@class="avator-wrap-s"]/img/@src').get()
        composer['name'] = response.xpath(
            '//p[contains(@class, "creator-name")]/text()').get()
        composer['intro'] = response.xpath(
            '//p[contains(@class, "creator-desc")]/text()').get()
        composer['like_counts'] = ci(response.xpath(
            '//span[contains(@class, "like-counts")]/text()').get())
        composer['fans_counts'] = ci(response.xpath(
            '//span[contains(@class, "fans-counts")]/@data-counts').get())
        composer['follow_counts'] = ci(response.xpath(
            '//span[@class="follow-wrap"]/span[2]/text()').get())
        # 取出class属性中包含icon-location的span节点相邻的下一个span节点内的文本
        composer['location'] = response.xpath(
            '//span[contains(@class, "icon-location")]/'
            'following-sibling::span[1]/text()').get() or ''
        composer['career'] = response.xpath(
            '//span[contains(@class, "icon-career")]/'
            'following-sibling::span[1]/text()').get() or ''
        yield composer

    def parse_video(self, response):
        """处理视频接口的数据"""
        resp = json.loads(response.text)
        post = response.meta['post']
        post['video'] = resp['data']['resource']['default']['url']
        post['preview'] = resp['data']['video']['cover']
        post['duration'] = resp['data']['video']['duration']
        yield post

    def parse_comment(self, response):
        """处理评论的接口"""
        resp = json.loads(response.text)
        comment_list = resp['data']['list']
        for comment in comment_list:
            c = CommentItem()
            c['commentid'] = comment['commentid']
            c['pid'] = comment['articleid']
            c['content'] = comment['content']
            c['created_at'] = comment['addtime_int']
            c['like_counts'] = ci(comment['count_approve'])
            c['cid'] = comment['userInfo']['userid']
            c['avatar'] = comment['userInfo']['face']
            c['uname'] = comment['userInfo']['username']
            # 判断本条评论是否是回复的之前的评论
            if comment['reply']:
                # 将reply字段设置为被回复的评论ID
                c['reply'] = comment['reply']['commentid']
            yield c
        next_page =  resp['data']['next_page_url']
        if next_page:
            yield response.follow(next_page, self.parse_comment)
















