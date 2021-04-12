#!/usr/bin/env python
# coding:utf-8
"""
启动所有爬虫
"""
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerRunner, CrawlerProcess

from scrapy import signals
from scrapy.utils.project import get_project_settings
import logging
import time
from scrapy.settings import Settings
from scrapy.signalmanager import SignalManager
from scrapy import signals
import time
import os
from kafka import KafkaProducer, producer
import types
import json
from pydispatch import dispatcher


class SpiderRunner(object):
    producer = None
    topic = 'bbs'

    def __init__(self, settings, *args):
        self.settings = settings
        self.runner = CrawlerProcess(self.settings)
        self.logger = logging.getLogger("SpiderRunner")
        # self.signals = SignalManager(self)
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip', value_serializer=lambda v: json.dumps(dict(v), default=str).encode('utf-8'))
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)
        dispatcher.connect(self.item_scraped, signal=signals.item_scraped)
        dispatcher.connect(self.spider_error, signal=signals.spider_error)

    def run_all(self):
        arrSpider = self.runner.spider_loader.list()
        arrSpider = [x for x in arrSpider if not x.endswith('_')]
        n = 0
        for spname in arrSpider:
            self.crawl_spider(spname)
        self.runner.start(False)

    def crawl_spider(self, spider_name):
        crawl = self.runner.create_crawler(spider_name)
        self.runner.crawl(crawl)

    # def create_crawler(self,spider):
    #     crawl = self.runner.create_crawler(spider_name)

    #     return crawl

    def spider_opened(self, spider):
        self.logger.info('spider opend: %s,%s', spider.name, spider.spider_tags)

    def spider_closed(self, spider, reason):
        if reason == 'finished':
            reactor.callLater(60*5, self.crawl_spider, spider.name)

    def item_scraped(self, item, response, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.item_scraped(each, response, spider)
        else:
            self.send_item(item)
            return item

    def send_item(self, item):
        self.logger.info('send item {spider},{title},{url}'.format(**{
            'spider': item['spider'],
            'title': item['title'],
            'url': item['url'],
        }))
        self.producer.send(self.topic, value=item)

    def spider_error(self, failure, response, spider):
        self.logger.info('spider_error %s,%s,%s', failure, response, spider)


def logging_configurer():
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')
    root = logging.getLogger()
    h = logging.handlers.RotatingFileHandler('logs/log.txt', 'a', 1024*1024*10, 10)
    f = logging.Formatter('%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    h.setLevel(logging.WARNING)
    root.addHandler(h)
    logging.getLogger('elasticsearch').addFilter(lambda r: r.levelno > logging.WARNING)
    logging.getLogger('scrapy.core.engine').addFilter(lambda r: r.levelno >= logging.WARNING)
    logging.getLogger('scrapy.middleware').addFilter(lambda r: r.levelno >= logging.WARNING)
    logging.getLogger('scrapy.crawler').addFilter(lambda r: r.levelno >= logging.WARNING)


def get_settings():
    settings = get_project_settings().copy()
    if 'crawl2020.pipelines.KafkaPipeline' in settings.get('ITEM_PIPELINES'):
        del settings.get('ITEM_PIPELINES')['crawl2020.pipelines.KafkaPipeline']
    settings.set('DUPEFILTER_CLASS', 'crawl2020.elasticSearchDupeFilter.ElasticSearchDumpFilter')
    settings.set('LOG_LEVEL', logging.INFO)
    return settings


if __name__ == "__main__":
    # main()
    logging_configurer()
    runner = SpiderRunner(get_settings())
    runner.run_all()
