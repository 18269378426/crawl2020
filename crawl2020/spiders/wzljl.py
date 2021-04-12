import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
import time


class WzljlSpider(BaseSpider):
    name = 'wzljl'
    source_name = '梧州零距离'
    allowed_domains = ['wz.wzljl.cn', 'www.wzljl.cn']
    spider_tags = ['梧州']
    start_urls = [
        'http://wz.wzljl.cn/',
        'http://www.wzljl.cn/node_440.htm',
        'http://www.wzljl.cn/node_8654.htm',
        'http://www.wzljl.cn/node_3780.htm'
    ]
    rules = [Rule(LinkExtractor(allow=(r'/\?mdl=topic&do=view&id=\d+')), callback='parse_item1', follow=False),
             Rule(LinkExtractor(allow=(r'http://www.wzljl.cn/content/\d+-\d+/\d+/content_\d+.htm')), callback='parse_item2', follow=False),
             Rule(LinkExtractor(allow=(r'https://mp.weixin.qq.com/s/\w+')), callback='parse_item3', follow=False),
             ]

    def parse_item1(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.content h1::text').extract_first()

        item['taskName'] = "http://www.wzljl.cn/templateRes/201011/05/2730/2730/logo.jpg"

        item['postBy'] = response.css('.content .wz_con span::text')[1].get()

        item['postOn'] = response.css('.content .wz_con em::text').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')[0]

        item['text'] = ''.join(response.css('.wz_con_dd *::text').extract())

        return item

    def parse_item2(self, response):
        item = self.createItem(response)

        item['title'] = response.css('.zbt::text').extract_first()

        item['postBy'] = response.css('[align=right]::text').extract_first()[3:]

        item['postOn'] = response.css('.z03::text').extract_first().strip() + ":00"

        item['text'] = ''.join(response.css('td p *::text').extract())

        return item

    def parse_item3(self, response):
        item = self.createItem(response)

        item['title'] = response.css('.rich_media_title::text').extract_first()

        item['postBy'] = response.css('section[powered-by=xiumi.us]::text')[-1]

        # 三种格式时间
        postOn = response.css('#publish_time::text')[0]
        postOn1 = postOn.re(r'\d{4}\-\d{1,2}\-\d{1,2}')

        if not postOn1:
            postOn1 = postOn.re(r'\d+小')
            num = 3600
            if not postOn1:
                postOn1 = postOn.re(r'\d+ 天')[0]
                num = 3600*24
            else:
                postOn1 = postOn1[0]
            past_time = int(postOn1[:-1]) * num
            postOn1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())-past_time))
        else:
            postOn1 = postOn1[0]+' 00:00:00'

        item['text'] = ''.join(response.css('.rich_media_content *::text').extract())

        return item
