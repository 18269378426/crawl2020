import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging


class Gc520Spider(BaseSpider):
    name = 'gc520'
    source_name = '恭城520'
    allowed_domains = ['www.gc520.cn']
    spider_tags = ['广西', '桂林', '恭城', '论坛']
    start_urls = [
        'http://www.gc520.cn/forum-2-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'http://www.gc520.cn/thread-\d+-1-1.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        if response.css('.alert_info p::text').extract():
            self.log('抱歉，本帖要求阅读权限高于 10 才能浏览：' + response.url, logging.INFO)
            return None

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('.authi .xw1::text').extract_first()

        postOn = response.css('.pti em span::attr(title)').extract_first()
        if not postOn:
            postOn = response.css('.pti em::text').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')[0]
        item['postOn'] = postOn

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
