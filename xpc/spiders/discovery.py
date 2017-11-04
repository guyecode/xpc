# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from xpc.items import PostItem, ComposerItem, CommentItem, CopyrightItem
from scrapy.exceptions import CloseSpider
from xpc.utils import convert_int as ci, strip


class PostsSpider(scrapy.Spider):
    name = 'posts'
    allowed_domains = ['www.xinpianchang.com']
    # 热门
    # start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']
    # 最新
    start_urls = ['http://www.xinpianchang.com/channel/index/id-0/sort-addtime/type-0']
    custom_settings = {
        'ITEM_PIPELINES': {
            'xpc.pipelines.PostPipeline': 300,
            'xpc.pipelines.ComposerPipeline': 301,
            'xpc.pipelines.CommentPipeline': 302,
            'xpc.pipelines.CopyrightItemPipeline': 303,
        }
    }

    def parse(self, response):
        self.logger.info('%s %s %s ' % (response.status, len(response.text), response.url))
        post_url = 'http://www.xinpianchang.com/a%s?from=channel'
        post_list = response.xpath('//ul[@class="video-list"]/li')
        # post_list = response.xpath('//ul[@class="video-list"]/li/@data-articleid').extract()
        for post in post_list:
            post_id = post.xpath('./@data-articleid').extract_first()
            request = Request(post_url % post_id, callback=self.parse_post)
            request.meta['pid'] = post_id
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').extract_first()
            yield request

        next_page = response.xpath('//div[@class="page"]/span[@class="current"]/following-sibling::a[1]/@href').extract_first()
        self.logger.info('next_page: %s' % next_page)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_post(self, response):
        # 提取作品信息
        post = PostItem()
        post['pid'] = response.meta['pid']
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').extract_first()
        post['thumbnail'] = response.meta['thumbnail']
        post['preview'] = strip(response.xpath('//div[@class="filmplay"]//img').extract_first())
        video = response.xpath('//video[@id="xpc_video"]/@src') or response.xpath('//div[@class="td-player"]//video/@src')
        post['video'] = video.extract_first()
        post['video_format'] = strip(response.xpath('//span[contains(@class, "video-format")]/text()').extract_first())
        post['category'] = response.xpath('//span[@class="cate v-center"]/text()').extract_first()
        post['created_at'] = response.xpath('//span[contains(@class,"update-time")]/i/text()').extract_first()
        post['play_counts'] = ci(response.xpath('//i[contains(@class,"play-counts")]/@data-curplaycounts').extract_first())
        post['like_counts'] = ci(response.xpath('//i[contains(@class,"like-counts")]/@data-counts').extract_first())
        post['description'] = strip(response.xpath('//p[contains(@class,"desc")]/text()').extract_first(default=''))
        yield post

        # 抓取评论
        comment_api = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi/id-%s/page-1'
        request = Request(comment_api % (post['pid']), callback=self.parse_comment)
        yield request

       
        composer_url = 'http://www.xinpianchang.com/u%s'
        composers = []
        for elem in response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li'):
            cid = elem.xpath('.//a[@class="head-wrap"]/@data-userid').extract_first()
            # 抓取作者信息
            request = Request(composer_url % cid, callback=self.parse_composer)
            request.meta['cid'] = cid
            yield request

            # 提取著作权信息
            cr = CopyrightItem()
            cr['pid'] = post['pid']
            cr['cid'] = cid
            cr['pcid'] = '%s_%s' % (cr['pid'], cid)
            cr['roles'] = elem.xpath('.//span[contains(@class, "roles")]/text()').extract_first()
            yield cr

    def parse_comment(self, response):
        result = json.loads(response.text)
        comments = result['data']['list']
        for c in comments:
            comment = CommentItem()
            comment['commentid'] = c['commentid']
            comment['pid'] = c['articleid'] or 0
            comment['cid'] = c['userInfo']['userid'] or 0
            comment['avatar'] = c['userInfo']['face']
            comment['uname'] = strip(c['userInfo']['username'])
            comment['created_at'] = c['addtime']
            comment['content'] = c['content']
            comment['like_counts'] = c['count_approve']
            if c['reply']:
                comment['reply'] = c['reply']['commentid'] or 0
            yield comment

        # 是否还有更多评论，有则继续抓取
        next_page = result['data']['next_page_url']
        if next_page:
            yield response.follow(next_page)

    def parse_composer(self, response):
        composer = ComposerItem()
        composer['cid'] = response.meta['cid']
        composer['name'] = response.xpath('//p[contains(@class,"creator-name")]/text()').extract_first()
        composer['banner'] = response.xpath('//div[@class="banner-wrap"]/@style').extract_first()[21:-1]
        _elem = response.xpath('//span[@class="avator-wrap-s"]')
        composer['avatar'] = _elem.xpath('./img/@src').extract_first()
        composer['verified'] = bool(_elem.xpath('.//span[@class="author-v yellow-v"]'))
        composer['intro'] = strip(response.xpath('//p[contains(@class,"creator-desc")]/text()').extract_first())
        composer['like_counts'] = ci(response.xpath('//span[contains(@class,"like-counts")]/text()').extract_first())
        composer['fans_counts'] = ci(response.xpath('//span[contains(@class,"fans-counts")]/text()').extract_first())
        composer['follow_counts'] = ci(response.xpath('//span[@class="follow-wrap"]/span[2]/text()').extract_first())

        yield composer
















