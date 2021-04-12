from ..baseSpider import BaseSpider
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class PtjgjNnyshSpider(BaseSpider):
    name = 'ptjgj_nnysh'
    source_name = '南宁夜生活'
    spider_tags = ['广西', '南宁', '新闻']
    allowed_domains = ['www.ptjgj.cn']
    start_urls = ['http://www.ptjgj.cn/nnjy/',
                  'http://www.ptjgj.cn/nnms/',
                  'http://www.ptjgj.cn/nnjd/',
                  'http://www.ptjgj.cn/nnjb/',
                  'http://www.ptjgj.cn/nnys/',
                  'http://www.ptjgj.cn/nnrd/'
                  ]

    rules = [Rule(LinkExtractor(allow=(r'/[a-zA-Z]{4}/\d+.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('div.title>center>h1::text').extract_first()

        item['taskName'] = "http://www.ptjgj.cn/html5_blue/images/logo.png"

        try:
            item['postBy'] = response.css('.subtitle>span::text').extract()[-1].strip()
        except:
            item['postBy']=''

        item['postOn'] = response.css('.subtitle>span:first-child::text').extract_first().replace('年', '')\
            .replace('月', '').replace('日', '').replace('时', '').replace('分', '').replace('秒', '')

        item['text'] = ''.join(response.css('.article_content>p::text').extract())

        return item
