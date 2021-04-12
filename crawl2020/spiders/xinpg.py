import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class XinpgSpider(BaseSpider):
    name = 'xinpg'
    source_name = '新平果'
    allowed_domains = ['www.xinpg.com', 'bbs.xinpg.com']
    spider_tags = ['广西', '百色', '苹果', '论坛']
    start_urls = [
        'http://www.xinpg.com/forum-34-1.html',
        'http://www.xinpg.com/forum-107-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'http://bbs.xinpg.com/thread-\d+-\d+-\d+.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.avatar img::attr(src)').extract_first()

        item['postBy'] = response.css('.authi a.xw1::text').extract_first()

        postOn = response.css('.pti .authi em::text').extract_first()
        if postOn:
            item['postOn'] = postOn[0]
        else:
            item['postOn'] = response.css('.pti .authi em span::attr(title)').extract_first()

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
