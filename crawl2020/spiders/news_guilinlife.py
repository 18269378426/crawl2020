import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class NewsGuilinlifSpider(BaseSpider):
    name = 'news_guilinlife'

    source_name = '桂林生活网'
    spider_tags = ['广西', '桂林', '新闻']
    allowed_domains = ['news.guilinlife.com']
    start_urls = ['http://news.guilinlife.com/guilin/',
                  'http://news.guilinlife.com/guangxi/',
                  'http://news.guilinlife.com/county/',
                  'http://news.guilinlife.com/original/']

    rules = [Rule(LinkExtractor(allow=(r'http://news.guilinlife.com/n/\d+-\d+/\d+/\d+.shtml')), callback='parse_item', follow=False)]

    def parse_item(self, response):
        if '提示信息' in response.css('title::text').extract_first():
            self.log('指定的主题不存在或已被删除或正在被审核：' + response.url, logging.INFO)
            super().dot_crawl_url(response.url)
            return None

        item = self.createItem(response)

        item['title'] = ' '.join(response.css('.article-title::text').extract())

        item['taskName'] = "http://statics.guilinlife.com/news/theme/img/logo.png"

        postBy = response.css('div.article-about>span:nth-of-type(1) a::text').extract_first()
        if postBy:
            item['postBy'] = postBy
        else:
            item['postBy'] = response.css('div.article-about>span::text').extract_first()[3:]

        item['postOn'] = response.css('div.article-about>span:nth-of-type(2)::text').extract_first()

        item['text'] = ''.join(response.css('.article-content *::text').extract())

        return item
