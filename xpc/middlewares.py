# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy.exceptions import NotConfigured


class RandomProxyMiddleware(object):
    """随机动态IP代理池"""

    def __init__(self, settings):
        # 2. 判断是否配置了IP代理池
        if not settings.getlist('PROXIES'):
            raise NotConfigured
        # 从配置里读取出来
        self.proxies = settings.getlist('PROXIES')
        # 设置代理IP的错误统计，默认设置为0
        self.stats = {}.fromkeys(self.proxies, 0)
        # 最大失败次数
        self.max_failed = 3

    @classmethod
    def from_crawler(cls, crawler):
        # 1. 首先判断是否启用了proxy
        if not crawler.settings.getbool('HTTPPROXY_ENABLED'):
            raise NotConfigured
        # 创建中间件对象
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # 3. 随机设置一个代理
        # 通过设置meta内的proxy属性，利用系统本身的proxy中间件去实现代理
        if 'proxy' not in request.meta:
            proxy_url = random.choice(self.proxies)
            request.meta['proxy'] = proxy_url

    def remove_proxy(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            print('proxy %s removed from proxies list' % proxy)

    def process_response(self, request, response, spider):
        # 4. 代理正常，但对方服务器返回了错误的状态码，有可能是被封掉
        cur_proxy = request.meta['proxy']
        if response.status != 200:
            print('none 200 status code: %s when use %s'
                  % (response.status, cur_proxy))
        if response.status >= 400:
            self.stats[cur_proxy] += 1
        # 如果异常status在该代理上出现了N次，也从代理池中删除
        if self.stats[cur_proxy] >= self.max_failed:
            self.remove_proxy(cur_proxy)
            # 删除当前request对象的代理，并返回重新调度下载
            del request.meta['proxy']
            return request
        # 如果一切正常，返回response对象，以让下面的中间件继续执行。
        return response

    def process_exception(self, request, exception, spider):
        # 4. 如果代理不可用，则会触发此方法
        cur_proxy = request.meta['proxy']
        # print一下异常信息
        print('raise exception: %s when use %s' % (exception, cur_proxy))
        # 从代理池中删除该代理
        self.remove_proxy(cur_proxy)
        # 删除当前request对象的代理，并返回重新调度下载
        del request.meta['proxy']
        return request