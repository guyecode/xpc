# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider
from xpc.items import PostItem, CommentItem, ComposerItem, CopyrightItem

def strip(s):
    """去掉字符串中特殊符号"""
    if s:
        return s.strip().replace('&nbsp;', '').replace('\xa0', '')
    return ''


def convert_int(s):
    """去掉数字字符串中的逗号，并将其转换成int类型"""
    if not s:
        return 0
    return int(s.replace(',', ''))
ci = convert_int


class DiscoverySpider(RedisSpider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com']
    # start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']
    # start_urls = ['http://www.xinpianchang.com/channel/index/type-0/sort-like/duration_type-0/resolution_type-/page-20']

    def start_requests(self):
        """重写默认的start_requests方法，以yield自定义的request对象"""
        for url in self.start_urls:
            yield Request(url, dont_filter=True, meta={'dont_merge_cookies': True})

    def make_requests_from_url(self, url):
        """ This method is deprecated. """
        return Request(url, dont_filter=True, meta={'dont_merge_cookies': True})

    def parse(self, response):
        url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
        # 取出列表页所有的视频节点
        posts = response.xpath('//ul[@class="video-list"]/li')
        # 循环遍历所有的节点，每一个节点对应一个视频
        for post in posts:
            # 取出视频的ID
            pid = post.xpath('./@data-articleid').extract_first()
            # 根据ID拼接出视频详情页的url
            request = Request(url % pid, callback=self.parse_post)
            # 利用request.meta属性的作用，将pid传递给回调函数
            request.meta['pid'] = pid
            # 将列表页的缩略图传递给回调函数
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            # 取一下播放时长
            duration = post.xpath('.//span[contains(@class, "duration")]/text()').get()
            # 把页面的显示时长（02' 46''）转换成int秒数
            minutes, seconds, *_ = duration.splti("'")
            request.meta['duration'] = ci(minutes) * 60 + ci(seconds)
            yield request
        # 获取底部翻页区内的所有链接，scrapy会自动过滤掉重复链接
        next_pages = response.xpath('//div[@class="page"]/a/@href').extract()
        for next_page in next_pages:
            # 给request.meta里面加上dont_merge_cookies属性
            # 以告诉scrapy框架强制使用我们自己设定的cookies
            yield Request(next_page,
                          callback=self.parse,
                          meta={'dont_merge_cookies': True})

    def parse_post(self, response):
        # 创建一个Item对象
        post = PostItem()
        # 取出上一步函数中传递过来的值
        post['pid'] = response.meta['pid']
        post['thumbnail'] = response.meta['thumbnail']
        # 提取出预览图
        post['preview'] = response.xpath(
            '//div[@class="filmplay"]//img/@src').get()
        # 视频URL
        post['video'] = response.xpath(
            '//a[@id="player"]/@href').get()
        # 视频播放时长
        post['duration'] = response.meta['duration']
        # 视频标题
        post['title'] = response.xpath(
            '//div[@class="filmplay-info"]//h3/text()').get()
        # 视频分类，由于取出的是多个，需要先strip，再join
        category = response.xpath(
            '//span[contains(@class, "cate")]//text()').extract()
        post['category'] = ''.join([strip(c) for c in category]).strip()
        # 创建时间
        post['created_at'] = response.xpath(
            '//span[contains(@class, "update-time")]/i/text()').get()
        # 播放次数
        post['play_counts'] = ci(response.xpath(
            '//i[contains(@class, "play-counts")]/@data-curplaycounts').get())
        # 该视频被点赞次数
        post['like_counts'] = ci(response.xpath(
            '//span[contains(@class, "like-counts")]/@data-counts').get())
        # 描述
        post['description'] = strip(response.xpath(
            '//p[contains(@class, "desc")]/text()').get())
        yield post

        # 作者的url模板
        url = 'http://www.xinpianchang.com/u%s?from=articleList'
        # 取出所有的作者节点
        composers = response.xpath('//div[@class="user-team"]//ul[@class="creator-list"]/li')
        for composer in composers:
            # 取出作者的ID
            cid = composer.xpath('./a/@data-userid').get()
            # 提取作者与视频的对应关系
            copyright = CopyrightItem()
            copyright['cid'] = cid
            copyright['pid'] = post['pid']
            # 联合主键，保证Item的唯一性
            copyright['pcid'] = '%s_%s' % (cid, post['pid'])
            copyright['roles'] = composer.xpath(
                './/span[contains(@class, "roles")]/text()').get() or ''
            yield copyright
            # 拼装成作者的主页URL，并创建request对象
            request = Request(url % cid, callback=self.parse_composer)
            # 把cid传递给回调函数
            request.meta['cid'] = cid
            yield request

        # 抓取异步加载的评论信息，根据ajax参数可以指定返回html还是json
        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&ajax=0&page=1'
        request = Request(comment_url % post['pid'], callback=self.parse_comment)
        yield request

    def parse_composer(self, response):
        composer = ComposerItem()
        composer['cid'] = response.meta['cid']
        # 取一下用户主责的背景大图
        background = response.xpath('//div[@class="banner-wrap"]/@style').get()
        # 因为大图是写在css样式里的，所以用切片操作提出出来
        composer['banner'] = background[21:-1]
        # 用户头像
        composer['avatar'] = response.xpath(
            '//span[@class="avator-wrap-s"]/img/@src').get()
        # 用户名称
        composer['name'] = response.xpath(
            '//p[contains(@class, "creator-name")]/text()').get()
        # 自我介绍
        composer['intro'] = response.xpath(
            '//p[contains(@class, "creator-desc")]/text()').get()
        # 用户人气，也就是被点赞的次数总和
        composer['like_counts'] = ci(response.xpath(
            '//span[contains(@class, "like-counts")]/text()').get())
        # 关注他的用户的数量
        composer['fans_counts'] = ci(response.xpath(
            '//span[contains(@class, "fans-counts")]/text()').get())
        # 他关注其他用户的数量
        composer['follow_counts'] = ci(response.xpath(
            '//span[@class="follow-wrap"]/span[2]/text()').get())
        # 所在位置
        composer['location'] = strip(response.xpath(
            '//span[contains(@class, "icon-location")]/'
            'following-sibling::span[1]/text()').get())
        # 职业
        composer['career'] = response.xpath(
            '//span[contains(@class, "icon-career")]/'
            'following-sibling::span[1]/text()').get()
        yield composer

    def parse_comment(self, response):
        # 直接加载json结果
        result = json.loads(response.text)
        comments = result['data']['list']
        for c in comments:
            comment = CommentItem()
            comment['pid'] = c['articleid']
            comment['cid'] = c['userInfo']['userid']
            comment['uname'] = c['userInfo']['username']
            comment['avatar'] = c['userInfo']['face']
            comment['commentid'] = c['commentid']
            comment['content'] = c['content']
            comment['created_at'] = c['addtime']
            comment['like_counts'] = c['count_approve']
            # 判断本条评论是否是回复其他的评论
            if c['reply']:
                # 如果是，把回复的那条评论的ID保存下来
                comment['reply'] = c['reply']['commentid'] or 0
            yield comment
        # 判断评论是否有下一页
        next_page = result['data']['next_page_url']
        if next_page:
             yield Request(next_page, callback=self.parse_comment)