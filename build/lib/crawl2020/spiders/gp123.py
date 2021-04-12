import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging


class Gp123Spider(BaseSpider):
    name = 'gp123'
    source_name = '桂平同城论坛'
    allowed_domains = ['www.gp123.cc']
    spider_tags = ['广西', '贵港', '桂平', '论坛']
    start_urls = [
        'http://www.gp123.cc/forum.php?mod=forumdisplay&fid=2'
    ]
    rules = [Rule(LinkExtractor(allow=(r'http://www.gp123.cc/forum.php\?mod=viewthread&tid=\d+&extra=page%3D1$')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        if response.css('.alert_error p::text').extract():
            self.log('没有找到帖子：' + response.url, logging.INFO)
            return None

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('.authi .xw1::text').extract_first()

        item['postOn'] = response.css('.pti em::text').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}')[0] + ':00'

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
