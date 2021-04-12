import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class BbsNgzbSpider(BaseSpider):
    name = 'bbs_ngzb'
    source_name = '南国早报论坛'
    allowed_domains = ['bbs.ngzb.com.cn']
    spider_tags = ['广西', '南宁', '论坛']
    start_urls = [
        'http://bbs.ngzb.com.cn/forum-72-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'https://bbs.ngzb.com.cn/thread-\d+-\d+-\d+.html')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        if (len(item['title']) == 0):
            self.log('error: 获取不到帖子标题,' + response.url, logging.DEBUG)
            return None

        item['taskName'] = response.css('.circle-avatar img::attr(src)').extract_first()

        item['postBy'] = response.css('.authi .xw1::text').extract_first()

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
