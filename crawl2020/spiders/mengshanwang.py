import logging
import scrapy
from datetime import datetime
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisSpider#导入RedisSpider

class MengshanWangSpider(RedisSpider):
    name = 'mengshanwang'
    source_name = '蒙山网论坛'
    allowed_domains = ['www.mengshanwang.cn']
    spider_tags = ['广西', '蒙山', '论坛']
    start_urls = [
                  'https://www.mengshanwang.cn/forum-95-1.html']

    rules = [Rule(LinkExtractor(allow=(r'thread-\d+-1-1.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = ' '.join(response.css('#thread_subject *::text').extract())

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('a.xw1::text').extract_first()

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

        text = [y for y in [x.strip() for x in response.css('td.t_f *::text').extract()] if y != '']
        item['text'] = '\n'.join(text)

        return item
