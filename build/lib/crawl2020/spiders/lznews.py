import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class LznewsSpider(BaseSpider):
    name = 'lznews'
    source_name = '柳州新闻网（今日柳州）'
    allowed_domains = ['www.lznews.gov.cn']
    spider_tags = ['广西', '柳州', '新闻']
    start_urls = [
        'http://www.lznews.gov.cn/article/2eee4bf7-4269-4492-8622-669a0f34ac44/index.aspx'

    ]
    rules = [Rule(LinkExtractor(allow=(r'/article/2eee4bf7-4269-4492-8622-669a0f34ac44/\d+.aspx')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.detailtitle h1::text').extract_first()

        item['taskName'] = "http://www.lznews.gov.cn/ad/%E6%96%B0%E9%97%BB%E5%8F%91%E5%B8%83%E4%BC%9A%E5%8D%8A%E9%80%9A%E6%A0%8F.jpg"

        item['postBy'] = response.css('.detailtitle span')[2].xpath('string(.)').extract_first()[3:]

        item['postOn'] = response.css('.detailtitle span::text')[1].re(r'\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0] + ':00'

        item['text'] = ''.join(response.css('.news_txt *::text').extract())

        return item
