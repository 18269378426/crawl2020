import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import re
import logging

class HongdouGxnewsSpider(BaseSpider):
    name = 'hongdou_gxnews'
    source_name = '红豆社区'
    allowed_domains = ['hongdou.gxnews.com.cn']
    spider_tags = ['广西','论坛']
    start_urls = [
        'http://hongdou.gxnews.com.cn/viewforum-1-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-50-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-21.html',
        'http://hongdou.gxnews.com.cn/viewforum-22.html',
        'http://hongdou.gxnews.com.cn/viewforum-23.html',
        'http://hongdou.gxnews.com.cn/viewforum-25.html',
        'http://hongdou.gxnews.com.cn/viewforum-24.html',
        'http://hongdou.gxnews.com.cn/viewforum-32.html',
        'http://hongdou.gxnews.com.cn/viewforum-27.html',
        'http://hongdou.gxnews.com.cn/viewforum-28.html',
        'http://hongdou.gxnews.com.cn/viewforum-26.html',
        'http://hongdou.gxnews.com.cn/viewforum-29.html',
        'http://hongdou.gxnews.com.cn/viewforum-30.html',
        'http://hongdou.gxnews.com.cn/viewforum-31.html',
        'http://hongdou.gxnews.com.cn/viewforum-45.html',
        'http://hongdou.gxnews.com.cn/viewforum-57.html',
        'http://hongdou.gxnews.com.cn/viewforum-349-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-356-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-387-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-388-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-391-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-392-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-393-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-394-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-395-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-396-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-397-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-398-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-399-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-400-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-401-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-402-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-403-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-404-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-405-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-407-1.html',
        'http://hongdou.gxnews.com.cn/viewforum-406-1.html'
    ]

    rules = [Rule(LinkExtractor(allow=(r'/viewthread-\d+.html$'), restrict_css='#nomalThread'), callback='parse_item', follow=False)]

    def parse_item(self, response):

        if not response.css('.thead *::text').extract():
            self.log('指定 主题 无效。如果您来自一个有效链接，请通知 管理员:' + response.url,logging.INFO)
            super().dot_crawl_url(response.url)
            return None
        item = self.createItem(response)

        title = ''.join(response.css('.thead *::text').extract()).strip()[3:]

        item['title'] = re.sub(r'\(您.+\)', '', title)

        item['taskName'] = response.css('.avatar_middle::attr(src)').extract_first()

        item['postBy'] = response.css('.posttable .green::text').extract_first()

        item['postOn'] = response.css('.alt1 [align=right]')[0].xpath('string(.)').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}')[0] + ':00'

        item['text'] = ''.join(response.css('.alt1 .viewmessage *::text').extract())

        return item