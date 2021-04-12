import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class QinzhouSpider(BaseSpider):
    name = 'qinzhou360'

    source_name = '钦州360'
    spider_tags = ['广西', '钦州', '论坛']
    allowed_domains = ['bbs.qinzhou360.com']
    start_urls = ['http://bbs.qinzhou360.com/forum-3-1.html']
    rules = [
        Rule(LinkExtractor(allow=(r'thread-\d+-1-1.html')), callback='parse_item', follow=False)
    ]

    def parse_item(self, response):
        if response.css('.alert_error p::text').extract():
            self.log('抱歉，指定的主题不存在或已被删除或正在被审核: ' + response.url, logging.INFO)
            super().dot_crawl_url(response.url)
            return None
        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('.pi .authi .xw1::text').extract_first()

        postOn = response.css('.pti em')
        if postOn:
            # 发表于 xxx小时前
            postOn1 = postOn[0].css('span::attr(title)').extract_first()
            if not postOn1:

                arr1 = postOn[0].re("\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}")
                if arr1:
                    postOn1 = arr1[0]

            if postOn1:
                item['postOn'] = datetime.strptime(postOn1, '%Y-%m-%d %H:%M:%S')

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
