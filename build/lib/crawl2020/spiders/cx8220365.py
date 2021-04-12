import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging


class Cx8220365Spider(BaseSpider):
    name = 'cx8220365'
    source_name = '岑溪人家论坛（市民爆料）'
    allowed_domains = ['www.8220365.com']
    spider_tags = ['广西', '岑溪', '论坛']
    start_urls = [
        'http://www.8220365.com/forum.php?mod=forumdisplay&fid=52'
    ]
    rules = [Rule(LinkExtractor(allow=(r'forum.php\?mod=viewthread&tid=\d+&extra=page%3D1')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('.pi .authi .xw1::text').extract_first()

        item['postOn'] = response.css('.pti .authi em::text').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')[0]

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
