from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class LipuSpider(BaseSpider):
    name = 'hepuwang'

    source_name = '合浦网（合浦生活）'

    spider_tags = ['广西', '合浦', '论坛']

    allowed_domains = ['bbs.hepuwang.com']

    start_urls = ['http://bbs.hepuwang.com/forum-2-1.html']

    rules = [Rule(LinkExtractor(allow=(r'thread-\d+-1-1.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        if '提示信息' in response.css('title::text').extract_first():
            self.log('指定的主题不存在或已被删除或正在被审核：' + response.url, logging.INFO)
            super().dot_crawl_url(response.url)
            return None

        item = self.createItem(response)

        item['title'] = ' '.join(response.css('#thread_subject::text').extract())

        if (len(item['title']) == 0):
            self.error('error: 获取不到帖子标题,' + response.url, logging.DEBUG)
            return None

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('div.authi>a::text').extract_first()

        item['postOn'] = response.css('.authi>em::text').extract_first()[4:] + ':00'

        item['text'] = '\n'.join([y for y in [x.strip() for x in response.css('td.t_f *::text').extract()] if y != ''])

        return item
