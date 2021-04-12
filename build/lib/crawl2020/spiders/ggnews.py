import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class GgnewsSpider(BaseSpider):
    name = 'ggnews'
    source_name = '贵港网络问政'
    allowed_domains = ['wz.ggnews.com.cn']
    spider_tags = ['广西', '贵港', '问政']
    start_urls = [
        'http://wz.ggnews.com.cn/',
        'http://wz.ggnews.com.cn/index.php?m=forum'
    ]
    rules = [Rule(LinkExtractor(allow=(r'index.php\?m=show&id=\d+')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.wz_nyt h1::text').extract_first()

        item['taskName'] = "http://wz.ggnews.com.cn/attach/2016/12/07/bd0b15f79c021d070240631a871cfcb7.gif"

        item['postBy'] = response.css('.wz_nyc li::text').extract_first()

        item['postOn'] = response.css('.wz_nyc li:last-child::text').extract_first()

        item['text'] = ''.join(response.css('.wz_nyb *::text').extract())

        return item
