import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging


class TengbeiSpider(BaseSpider):
    name = 'tengbei'
    source_name = '藤北网（资讯）'
    allowed_domains = ['www.tengbei.net']
    spider_tags = ['藤北']
    start_urls = [
        'http://www.tengbei.net/project/news'
    ]
    rules = [Rule(LinkExtractor(allow=(r'/project/news/show/\d+.html')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):

        if not response.css('h2.text-center::text').extract_first():
            self.log('找不到：' + response.url, logging.INFO)
            return None

        item = self.createItem(response)

        item['title'] = response.css('h2.text-center::text').extract_first()

        item['taskName'] = "http://www.tengbei.net/project/images/tlogo.png"

        item['postBy'] = response.css('p.text-center strong::text').extract_first()

        item['postOn'] = response.css('p.text-center *::text').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')[0]

        item['text'] = ''.join(response.css('.newscontent *::text').extract())

        return item
