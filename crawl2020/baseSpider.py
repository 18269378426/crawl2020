from pydispatch import dispatcher
from . import mysignals
import scrapy
from datetime import datetime, timedelta
from scrapy.spiders import CrawlSpider
from .items import CrawlItem
import pytz
import hashlib

tz = pytz.timezone('Asia/Shanghai')


class BaseSpider(CrawlSpider):
    name = ''
    source_name = ''
    task_name = ''
    spider_id = 0
    spider_tags = []
    tags = []

    def createItem(self, response):
        item = CrawlItem()
        item['url'] = response.url
        item['spider'] = self.name
        item['source'] = self.source_name
        item['crawlOn'] = datetime.now(tz)
        item['html'] = response.text
        item['spiderTags'] = self.spider_tags
        item['tags'] = self.tags
        item['id'] = hashlib.sha1(response.url.encode('utf-8')).hexdigest()
        return item

    def dot_crawl_url(self, url):
        dispatcher.send(mysignals.signal_ignore_url, None, url)

    def __str__(self):
        return 'spider[{0},{1}]'.format(self.name, self.source_name)
