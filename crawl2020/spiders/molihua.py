import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class MolihuaSpider(BaseSpider):
    name = 'molihua'
    source_name = '横县茉莉花网'
    allowed_domains = ['www.molihua.net']
    spider_tags = ['广西', '横县', '论坛']
    start_urls = [
        'http://www.molihua.net/forum-chafang-1.html',
        'http://www.molihua.net/forum-6-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'thread-\d+-\d+-\d+.html')), callback='parse_item', follow=False)
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

                arr1 = postOn[0].re(r"\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}")
                if arr1:
                    postOn1 = arr1[0]

            if postOn1:
                item['postOn'] = datetime.strptime(postOn1, '%Y-%m-%d %H:%M:%S')

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
