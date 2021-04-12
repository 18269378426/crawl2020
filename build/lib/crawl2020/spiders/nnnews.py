from ..baseSpider import BaseSpider
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class NnnewsSpider(BaseSpider):
    name = 'nnnews'
    source_name = '南宁新闻网'
    allowed_domains = ['www.nnnews.net']
    start_urls = [
        # 'http://www.nnnews.net/lvyou/index.html',
        'http://www.nnnews.net/jiaoyu/index.html',
        'http://www.nnnews.net/yaowen/index.html',
        'http://www.nnnews.net/xianqu/index.html'
    ]
    spider_tags = ['广西', '南宁', '新闻']

    rules = [Rule(LinkExtractor(allow=(r'http://www.nnnews.net/lvyou/p/\d+.html',
                                       r'http://www.nnnews.net/jiaoyu/p/\d+.html',
                                       r'http://www.nnnews.net/yaowen/p/\d+.html',
                                       r'http://www.nnnews.net/xianqu/p/\d+.html')),
                  callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('div.xiangqing_dabiaoti h2::text').extract_first()

        item['taskName'] = "http://res.nnnews.net/t/site/10001/bb0b54ebc21ac71db48a1637f89a43a0/assets//nny/list/images/liebiao_logo.jpg"

        item['postBy'] = response.css('div.fxandtime_left>ul>li:nth-child(2)>a::text').extract_first() or response.css('.editors::text').extract_first()

        try:
            item['postOn'] = response.css('div.fxandtime_left>ul>li:first-child::text').extract_first()+':00'
        except:
            item['postOn'] = response.css('.date::text').extract_first()+':00'
        
        
        item['text'] = ''.join(response.css('div.xiangqing_three_left p::text').extract())

        return item
