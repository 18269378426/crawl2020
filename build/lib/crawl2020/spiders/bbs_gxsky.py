import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class BbsGxskySpider(BaseSpider):
    name = 'bbs_gxsky'
    source_name = '时空网'
    allowed_domains = ['www.gxsky.com']
    spider_tags = ['广西', '南宁', '论坛']
    start_urls = [
        'https://www.gxsky.com/forum-32-1.html',
        'https://www.gxsky.com/forum-799-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'thread-\d+-1-1.html')), callback='parse_item', follow=False)
             ]

    def parse_item(self, response):
        if '提示信息' in response.css('title::text').extract_first():
            self.log('指定的主题不存在或已被删除或正在被审核：' + response.url, logging.INFO)
            self.dot_crawl_url(response.url)
            return None

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        if (len(item['title']) == 0):
            self.log('error: 获取不到帖子标题,' + response.url, logging.DEBUG)
            return None

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('.authi a::text').extract_first()

        postOn = response.css('.pti em')
        if postOn:
            # 发表于 xxx小时前
            postOn1 = postOn[0].css('span::attr(title)').extract_first()
            if not postOn1:

                arr1 = postOn[0].re("\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}")
                if arr1:
                    postOn1 = arr1[0]

            if postOn1:
                item['postOn'] = datetime.strptime(postOn1, '%Y-%m-%d %H:%M:%S')

        item['text'] = ''.join(response.css('.t_f *::text').extract())

        return item
