import scrapy
from ..baseSpider import BaseSpider
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor


class GxpeopleSpider(BaseSpider):
    name = "gxpeople"
    source_name = "广西人民网"
    allowed_domains = ["gx.people.com.cn"]
    spider_tags = ['广西', '南宁', '新闻']
    start_urls = ['http://gx.people.com.cn/']

    rules = [Rule(LinkExtractor(allow=(r'/n2/\d+/\d+/c\d+-\d+.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.text_title h1::text').extract_first()

        item['taskName'] = "http://www.people.com.cn/img/2016wb/images/logo01.png"

        item['postBy'] = response.css('div.box01 a::text').extract_first()

        # TODO: http://gx.people.com.cn/n2/2020/1031/c179430-34386403.html
        try:
            postOn = response.css('div.box01 div.fl::text').extract_first().split(' ')[0]
            postOn1 = postOn.replace('年', '-').replace('月', '-').replace('日', ' ')+':00'
            item['postOn'] = postOn1
        except:
            item['postOn'] = ''

        item['text'] = ''.join(response.css('div.box_con p::text').extract())

        return item
