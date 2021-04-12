import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class GongzhouSpider(BaseSpider):
    name = 'gongzhou'
    source_name = '平南龚州论坛'
    allowed_domains = ['www.gongzhou.com']
    spider_tags = ['广西', '贵港', '平南', '论坛']
    start_urls = [
        'http://www.gongzhou.com/forum.php?mod=forumdisplay&fid=5',
        'http://www.gongzhou.com/forum.php?mod=forumdisplay&fid=18'
    ]
    rules = [Rule(LinkExtractor(allow=(r'https://www.gongzhou.com/forum.php\?mod=viewthread&tid=\d+&extra=page%3D1')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avtm>img::attr(src)').extract_first()

        item['postBy'] = response.css('.authi .xw1::text').extract_first()

        item['postOn'] = response.css('.pti em span::text').extract_first() + ':00'

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
