# Scrapy settings for crawl2020 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawl2020'

SPIDER_MODULES = ['crawl2020.spiders']
NEWSPIDER_MODULE = 'crawl2020.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawl2020 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# HTTPERROR_ALLOWED_CODES = [301,302]

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# 设置调度器
SCHEDULER='scrapy_redis.scheduler.Scheduler'
# #设置去重过滤器
DUPEFILTER_CLASS='scrapy_redis.dupefilter.RFPDupeFilter'
# #设置连接Redis 的URL
REDIS_URL = 'redis://:foobared@localhost:6379'   #密码链接

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 2
#CONCURRENT_REQUESTS_PER_IP = 16

RETRY_ENABLED = False
REDIRECT_ENABLED = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
#    'crawl2020.middlewares.Crawl2020SpiderMiddleware': 543,
    # 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {   
   'crawl2020.middlewares.Crawl2020DownloaderMiddleware': 200,
   'crawl2020.middlewares.RotateUserAgentMiddleware':543,
#    'scrapy_splash.SplashCookiesMiddleware': 723,
#     'scrapy_splash.SplashMiddleware': 725,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}
# SPLASH_URL = 'http://localhost:8050'
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.logstats.LogStats': None,
    # 'scrapy.extensions.corestats.CoreStats': None,
    'scrapy.webservice.WebService': None
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'crawl2020.pipelines.Crawl2020Pipeline': 300,
# }
ITEM_PIPELINES = {
    # 'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500,
    'crawl2020.pipelines.ClearTextPipeline': 250,
    'crawl2020.pipelines.ConvertPostOnPipeline': 255,
    'crawl2020.pipelines.KafkaPipeline': 299,
    'crawl2020.pipelines.ElasticSearchPipeline': 300,
     'scrapy_redis.pipelines.RedisPipeline': 200,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# spider结束后不显示运行状态汇总
STATS_DUMP = False

import logging
LOG_LEVEL=logging.INFO
# LOG_FILE = "./log/log.txt"  # 保存在当前文件下
# 自定义


USER_AGENT_CHOICES = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:24.0) Gecko/20140205 Firefox/24.0 Iceweasel/24.3.0',
    'Mozilla/5.0 Windows NT 10.0; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 Windows NT 10.0; WOW64; rv:28.0) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
]


# elasticsearch  https://github.com/jayzeng/scrapy-elasticsearch
ELASTICSEARCH_SERVERS = ['localhost:9200']
# ELASTICSEARCH_SERVERS = ['es.test.fastoa.co:80']
ELASTICSEARCH_INDEX = 'scrapy'
# ELASTICSEARCH_INDEX_DATE_FORMAT = '%Y-%m'
ELASTICSEARCH_INDEX_DATE_FORMAT = '%Y'
# ELASTICSEARCH_UNIQ_KEY = 'url'  # Custom unique key
ELASTICSEARCH_BUFFER_LENGTH = 5
# ELASTICSEARCH_USERNAME = ''
# ELASTICSEARCH_PASSWORD = ''
# can also accept a list of fields if need a composite key
#ELASTICSEARCH_UNIQ_KEY = ['url', 'id']


# DUPEFILTER_CLASS='crawl2020.elasticSearchDupeFilter.ElasticSearchDumpFilter'
# DUPEFILTER_DEBUG=True
FEED_EXPORT_ENCODING = 'utf-8' 
TTPERROR_ALLOWED_CODES = [403]
