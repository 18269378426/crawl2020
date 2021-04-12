import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import time


class Td776Spider(BaseSpider):
    name = 'td776'
    source_name = '田东776论坛'
    allowed_domains = ['www.td776.com']
    spider_tags = ['广西', '百色', '田东', '论坛']
    start_urls = [
        'http://www.td776.com/forum-13-1.php'
    ]
    rules = [Rule(LinkExtractor(allow=(r'/thread/\d+.php')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('#thread_subject::text').extract_first()

        item['taskName'] = response.css('.lazy::attr(src)').extract_first()

        item['postBy'] = response.css('.authi a.xw1::text').extract_first()

        postOn = response.css('.pti .authi span span::text')[0]

        # 三种格式时间
        postOn1 = postOn.re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')

        try:
            if not postOn1:
                postOn1 = postOn.re(r'\d+小')
                num = 3600
                if not postOn1:
                    postOn1 = postOn.re(r'\d+天')[0]
                    num = 3600*24
                else:
                    postOn1 = postOn1[0]
                past_time = int(postOn1[:-1]) * num
                postOn1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())-past_time))
            else:
                postOn1 = postOn1[0]
            item['postOn'] = postOn1
        except  :
            item['postOn']=''

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
