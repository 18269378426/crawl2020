#!/usr/bin/env python3
# coding:utf-8
"""
启动爬虫
"""
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
import logging

from scrapy import signals
from scrapy.utils.project import get_project_settings
import logging 
from scrapy.settings import Settings
from scrapy.signalmanager import SignalManager


logger = logging.getLogger( __name__ )

def main():
    settings = get_project_settings()
    crawler = CrawlerProcess(settings)
    arrSpider = crawler.spider_loader.list()
    arrSpider = [x for x in arrSpider if not x.endswith('_') ]
    arrSpider = sorted( arrSpider )
    n=0
    for sn in arrSpider:
        sp = crawler.spider_loader.load(sn)
        print('{0}. {1}\t{2}'.format(n,sn,sp.source_name))
        n = n+1
    i = input('choice spider to run:')
    i = int(i)    
    spidername = arrSpider[i]
    runspider( spidername)

#    print( spidername)
def runspider(name):
    logger.info('start spider %s',name)
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    crawler = runner.create_crawler(name)
    
    crawler.signals.connect(spider_closed, signal=signals.spider_closed)
    
    d = runner.crawl(crawler)
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())

def spider_closed( spider, reason):
    logger.info('spider_closed: %s,%s', spider,reason)

if __name__ == "__main__": 
    main()
    reactor.run()
