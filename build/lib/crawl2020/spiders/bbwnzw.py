import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class BbwnzwSpider(BaseSpider):
    name = 'bbwnzw'
    source_name = '南珠网论坛'
    allowed_domains = ['www.bbwnzw.com']
    spider_tags = ['广西', '北海', '论坛']
    start_urls = [
        'https://www.bbwnzw.com/forum.php?mod=forumdisplay&fid=39'
    ]
    rules = [Rule(LinkExtractor(allow=(r'forum.php\?mod=viewthread&fid=\d+&tid=\d+&typeid=\d+&extra=page%3D1')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('.pi div a::text').extract_first()

        postOn = response.css('td.plc .pti .authi em span::attr(title)').extract_first()
        if postOn:
            item['postOn'] = postOn
        else:
            item['postOn'] = response.css('td.plc .pti .authi em::text').re(r"\d{4}-\d{1,2}-\d{1,2}")[0] + ' 00:00:00'

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
