# -*- coding: utf-8 -*-
import scrapy
from xpc.items import PostItem
from scrapy.exceptions import CloseSpider

class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['www.xinpianchang.com']
    # 热门
    # start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']
    # 最新
    start_urls = ['http://www.xinpianchang.com/channel/index/id-0/sort-addtime/type-0']

    def parse(self, response):
    	post_url = 'http://www.xinpianchang.com/a%s?from=channel'
        post_list = response.xpath('//ul[@class="video-list"]/li/@data-articleid').extract()
        for post in post_list:
        	request = scrapy.Request(post_url % post, callback=self.parse_post)
        	request.meta['pid'] = post
        	yield request



    def parse_post(self, response):
    	post = PostItem()
    	post['pid'] = response.meta['pid']
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').extract_first()
        post['category'] = response.xpath('//span[@class="cate v-center"]/text()').extract_first()
        post['created_at'] = response.xpath('//span[@class="update-time v-center"]').extract_first()
        post['play_count'] = response.xpath('//i[contains(@class,"play-counts")]/@data-curplaycounts').extract_first()
        post['like_count'] = response.xpath('//i[contains(@class,"like-counts")]/@data-counts').extract_first()
        post['description'] = response.xpath('//p[contains(@class,"desc")]/text()').extract_first(default='')

        comments = []
        for elem in response.xpath('//ul[@class="comment-list"]/li'):
    		comment = {}
    		comment['uid'] = elem.xpath('./a/span/@data-userid)').extract_first()
    		comment['avatar'] = elem.xpath('./a/span/img/@src').extract_first()
    		comment['uname'] = elem.xpath('.//span[contains(@class,"user-name")]/text()').extract_first()
    		comment['created_at'] = elem.xpath('.//span[contains(@class,"send-time")]/text()').extract_first()
    		comment['content'] = elem.xpath('.//div[contains(@class,"comment-con")]/text()').extract_first()
    		comment['like_count'] = elem.xpath('.//i[@class="approve-counts"]/i/text()")').extract_first()
    		comments.append(comment)
        post['comments'] = comments

        composer_url = 'http://www.xinpianchang.com/u%s'
    	composers = []
    	for elem in response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li'):
            cid = elem.xpath('.//a[@class="head-wrap"]/@data-userid').extract_first()
        	# yield response.follow(composer_url % cid, callback=self.parse_composer)
            composers.append({
    			'cid': cid,
    			'avatar': elem.xpath('.//a[@class="head-wrap"]/img/@src').extract_first(),
    			'name': elem.xpath('.//span[contains(@class, "name")]/text()').extract_first(),
    			'roles': elem.xpath('.//span[contains(@class, "roles")]/text()').extract_first(),
    			})
    	post['composers'] = composers
        yield post

    def parse_composer(self, response):
    	print response.url