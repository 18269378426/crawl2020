import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class GxbbsSpider(BaseSpider):
    name = 'gxbbs'
    source_name = '广西论坛'
    spider_tags = ['广西', '论坛']
    allowed_domains = ['www.gxbbs.cc']

    start_urls = [
        'http://www.gxbbs.cc/bbs-48-1',
        'http://www.gxbbs.cc/bbs-2-1',
        'http://www.gxbbs.cc/bbs-37-1'
    ]

    rules = [Rule(LinkExtractor(allow=(r'http://www.gxbbs.cc/thread-\d+-\d+-\d+.html'), restrict_css=('#threadlist')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.title-cont>a>span::text').extract_first()

        item['taskName'] = "http://www.gxbbs.cc/uc_server/images/noavatar_small.gif"

        item['postBy'] = response.css('.post-hd .name>span::text').extract_first()

        postOn = response.css('.uprestige.z+span.z::text')[0].re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')
        if postOn:
            postOn = postOn[0]
        else:
            postOn = response.css('.uprestige.z+span.z span::attr(title)').extract_first()

        item['postOn'] = postOn

        item['text'] = ''.join(response.css('.t_f *::text').extract())

        return item
