import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class By8Spider(BaseSpider):
    name = 'by8'
    source_name = '宾阳吧'
    allowed_domains = ['www.by8.cn']
    spider_tags = ['广西', '宾阳', '论坛']
    start_urls = [
        'https://www.by8.cn/forum-37-1.html',
        'https://www.by8.cn/forum-62-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'thread-\d+-\d+-\d+.html')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):

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
