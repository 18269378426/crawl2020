import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class FcgttSpider(BaseSpider):
    name = 'fcgtt'

    source_name = '防城港天天网'
    spider_tags = ['广西', '防城港', '新闻']
    allowed_domains = ['www.fcgtt.com']
    start_urls = ['https://www.fcgtt.com/article/']
    rules = [Rule(LinkExtractor(allow=(r'https://www.fcgtt.com/article/article_\d+.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.detail>h1::text').extract_first()

        item['taskName'] = "https://www.fcgtt.com/UploadFile/index/2020/5-11/202005110859003614300.jpg"

        item['postBy'] = response.css('div.publish>ul>li:nth-of-type(2)::text').extract_first()

        item['postOn'] = response.css('.publish >ul>li::text').extract_first()

        item['text'] = ''.join(response.css('#resizeIMG *::text').extract())

        return item
