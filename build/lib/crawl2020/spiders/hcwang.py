import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class HcwangSpider(BaseSpider):
    name = 'git'

    source_name = '河池论坛网络认证'

    spider_tags = ['广西', '河池', '新闻']

    allowed_domains = ['wlwz3.hcwang.cn']

    start_urls = ['http://wlwz3.hcwang.cn/']

    rules = [Rule(LinkExtractor(allow=(r'wentixx.asp.did=\d+')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        if '提示信息' in response.css('title::text').extract_first():
            self.log('指定的主题不存在或已被删除或正在被审核：' + response.url, logging.INFO)
            super().dot_crawl_url(response.url)
            return None

        item = self.createItem(response)

        item['title'] = ' '.join(response.css('font[color="#055779"]>strong::text').extract())

        if (len(item['title']) == 0):
            self.error('error: 获取不到帖子标题,' + response.url, logging.DEBUG)
            return None

        item['taskName'] = "http://wlwz3.hcwang.cn/images/cx_05.jpg"

        item['postBy'] = response.css('.minaa2 tr:nth-of-type(2)>td::text').extract()[1]

        item['postOn'] = response.css('.minaa2 tr:nth-of-type(2)>td::text').extract()[3]

        item['text'] = ''.join(response.css('.minaa2 *::text').extract()) + \
            ''.join(response.css('.minaa3 *::text').extract()) + \
            ''.join(response.css('.minaa4 *::text').extract())

        return item
