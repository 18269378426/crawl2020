#!/usr/bin/env python
# coding:utf-8
"""
启动所有爬虫
"""

from scrapy.crawler import CrawlerProcess

from scrapy import signals
from scrapy.utils.project import get_project_settings
import logging
from scrapy import signals
import sys
import time
import datetime

class SpiderRunner(object):
    def __init__(self):
        self.settings = get_project_settings()
        self.runner = CrawlerProcess(self.settings)
        self.logger = logging.getLogger("SpiderRunner")

    def get_all_spiders(self):
        return   CrawlerProcess(self.settings).spider_loader.list()

    def start(self, spiders):
        for spider_name in spiders:
            crawler = self.runner.create_crawler(spider_name)
            crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)
            crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
            crawler.signals.connect(self.spider_error, signal=signals.spider_error)
            crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
            self.runner.crawl(crawler)            
            self.logger.info('load spider: %s,%s',crawler.spider.name, crawler.spider.spider_tags)
        time.sleep(10)
        self.runner.start()

    def spider_closed(self, spider, reason):
        self.logger.info('spider_closed: %s', spider)

    def item_scraped(self, item, response, spider):
        self.logger.info('item_scraped %s  ',
                         {
                             'title': item['title'],
                             'url': response.url,
                             'spider': spider.name,
                             'spiderSource': spider.source_name
                         })

    def spider_error(self, failure, response, spider):
        self.logger.info('spider_error %s,%s,%s', failure, response, spider)

    def spider_opened(self, spider):
        self.logger.info('spider_opened  %s', spider)


runner = SpiderRunner()
spiders = [x for x in ','.join(sys.argv[1:]).split(',') if x != ''] if len(sys.argv) > 1 else runner.get_all_spiders()

def doSth():
    # print(spiders)
    SpiderRunner().start(spiders)

def main(h=9, m=30): #设置每天早上九点半爬取更新数据，检测到即刻运行
    while True:
        now = datetime.datetime.now()
        # print(now.hour, now.minute)
        if now.hour == h and now.minute == m:
            doSth()
        time.sleep(10)
main()