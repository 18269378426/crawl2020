import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class NntvSpider(BaseSpider):
    name = 'pbt'
    source_name = '老友网'
    allowed_domains = ['www.nntv.cn']
    spider_tags = ['广西', '南宁', '论坛']
    start_urls = [
        'http://www.nntv.cn/news/m/list.shtml',
        'http://www.nntv.cn/bl/list.shtml'

    ]
    rules = [Rule(LinkExtractor(allow=(r'/news/m/\d+-\d+-\d+/\d+.shtml')), callback='parse_item1', follow=False),
             Rule(LinkExtractor(allow=(r'/bl/bl_content_\d+.shtml')), callback='parse_item2', follow=False)
             ]

    def parse_item1(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.subject h1::text').extract_first()

        item['taskName'] = "http://www.nntv.cn/img/logo2014_white.png"

        item['postBy'] = response.css('.editor::text').extract_first()[5:-2]

        item['postOn'] = response.css('.time::text').extract_first() + ':00'

        item['text'] = ''.join(response.css('.contentText *::text').extract())

        return item

    def parse_item2(self, response):
        item = self.createItem(response)

        item['title'] = response.css('.content_left_header h3::text').extract_first()
        item['postBy'] = '老友网'
        item['postOn'] = response.css('.content_left_header p span::text').extract_first().replace('年', '-').replace('月', '-').replace('日', ' ') + '00:00:00'

        item['text'] = ''.join(response.css('.content_left_center *::text').extract())

        return item
