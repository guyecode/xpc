# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import redis
from scrapy.exceptions import NotConfigured


class RandomProxyMiddleware(object):
    """
    利用scrapy本身的proxy middle机制，实现一个随机IP代理池，并且可以动态的删除有问题的IP
    """

    def __init__(self, settings):
        # 2. 初始化中间件对象
        # 初始化redis
        self.redis = redis.Redis(host='127.0.0.1')
        self.redis_key = 'discovery:proxies'

        # 所有的代理,list类型
        # self.proxies = settings.getlist('PROXIES')
        # 所有的代理的失败次数统计
        self.stats_redis_key = 'discovery:proxies_stats'
        # 所有问题的代理放到一个list中
        self.failed_proxy_key = 'discovery:failed_proxies'
        # 最大失败次数
        self.max_failed = 3

    @classmethod
    def from_crawler(cls, crawler):
        # 1. 判断是否打开了代理，并且创建中间件对象
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # 3. 设置随机代理IP
        cur_proxy, = self.redis.srandmember(self.redis_key, 1)
        cur_proxy = cur_proxy.decode('utf-8')
        request.meta['proxy'] = cur_proxy
        print('use proxy: %s' % cur_proxy)

    def process_response(self, request, response, spider):
        # 4. 处理非正常的http返回码
        cur_proxy = request.meta['proxy']
        # 如果状态码大于400，我们认为可能是被对方封掉了
        if response.status >= 400:
            self.redis.hincrby(self.stats_redis_key, cur_proxy, 1)
            print('get http status %s when use proxy: %s' % \
                  (response.status, cur_proxy))

        # 如果返回400以上状态码的次数超过最大失败次数，则将该IP从代理池中删除
        failed_times = self.redis.hget(self.stats_redis_key, cur_proxy) or 0
        if int(failed_times) >= self.max_failed:
            self.remove_proxy(cur_proxy)
        # 记得返回response对象
        return response

    def process_exception(self, request, exception, spider):
        # 4. 处理请求过程中发和异常的情况
        # 通常是代理服务器本身挂掉了，或者网络原因
        cur_proxy = request.meta['proxy']
        print('raise exption: %s when use %s' % (exception, cur_proxy))
        # 直接从代理池中删除
        self.remove_proxy(cur_proxy)
        # 将IP从当前的request对象中删除
        del request.meta['proxy']
        # 从新安排该request调度下载
        return request

    def remove_proxy(self, proxy):
        # 从代理池中删除某个IP
        self.redis.srem(self.redis_key, proxy)
        print('proxy %s removed from proxies list' % proxy)
        self.redis.lpush(self.failed_proxy_key, proxy)