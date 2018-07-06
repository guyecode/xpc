# -*- coding: utf-8 -*-

# Scrapy settings for xpc project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xpc'

SPIDER_MODULES = ['xpc.spiders']
NEWSPIDER_MODULE = 'xpc.spiders'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://127.0.0.1:6379'
# 在redis中持久化爬虫状态
SCHEDULER_PERSIST = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
HTTPPROXY_ENABLED = True
DOWNLOAD_TIMEOUT = 10
RETRY_ENABLED = False
# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
    'Connection': "keep-alive",
    'Cookie': "bdshare_firstime=1529042870412; Device_ID=5b287a893cecb; _ga=GA1.2.1993306170.1529379466; zg_did=%7B%22did%22%3A%20%22164161eab2fa4e-0a721771121a41-17366952-13c680-164161eab30828%22%7D; UM_distinctid=16250e0aac3125-0f3fea18eb61d2-33627805-13c680-16250e0aac48d4; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22164161eab3d478-07ad870e634f5f-17366952-1296000-164161eab3e917%22%2C%22%24device_id%22%3A%22164161eab3d478-07ad870e634f5f-17366952-1296000-164161eab3e917%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; PHPSESSID=513re4n40d15ltbv59lkf6nvi7; Hm_lvt_dfbb354a7c147964edec94b42797c7ac=1529377605,1529377930,1529379466,1529934242; _gid=GA1.2.611501098.1530496147; CNZZDATA1262268826=782713340-1528694162-%7C1530579201; Authorization=55CCD98A4A4EF1D474A4EF45614A4EF9DBA4A4EF5AC7E9BADD4B; ts_uptime=0; visit_userid_10186378=1; _gat=1; zg_c9c6d79f996741ee958c338e28f881d0=%7B%22sid%22%3A%201530579738.775%2C%22updated%22%3A%201530581792.061%2C%22info%22%3A%201530496145845%2C%22cuid%22%3A%2010356603%7D; Hm_lpvt_dfbb354a7c147964edec94b42797c7ac=1530581792; responseTimeline=144; cn_1262268826_dplus=%7B%22distinct_id%22%3A%20%2216250e0aac3125-0f3fea18eb61d2-33627805-13c680-16250e0aac48d4%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201530581796%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201530581796%7D%7D",
    'DNT': "1",
    'Host': "www.xinpianchang.com",
    'Upgrade-Insecure-Requests': "1",
    'Cache-Control': "no-cache",
    }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'xpc.middlewares.XpcSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'xpc.middlewares.RandomProxyMiddleware': 749,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'xpc.pipelines.MysqlPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
