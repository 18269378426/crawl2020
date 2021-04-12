import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import time
import logging


class NgzbSpider(BaseSpider):
    name = 'ngzb'
    source_name = '南国早报网'
    spider_tags = ['广西', '南宁', '新闻']
    allowed_domains = ['www.ngzb.com.cn']
    start_urls = [
        'https://www.ngzb.com.cn/index.php/channel/7.html',
        'https://www.ngzb.com.cn/channel/1.html'

    ]

    rules = [Rule(LinkExtractor(allow=(r'/index.php/news/\d+.html', r'/news/\d+.html'), restrict_css=('.text-primary-dark')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        title = response.css('.newspage-main-title::text').extract_first()
        if (title == None):
            title = response.css('#thread_subject::text').extract_first()
        item['title'] = title

        item['taskName'] = "https://www.ngzb.com.cn/static/home/img/header_logo.png"

        postBy = response.css('.pti a::text').extract_first()
        if (postBy == None):
            try:
                postBy = response.css('span.newspage-main-info-meta-item4::text').extract()[1][3:]
            except:
                self.log('error: 获取不到帖子作者,' + response.url, logging.DEBUG)
                return None
        item['postBy'] = postBy

        postOn1 = response.css('.pti em span::attr(title)').extract_first()
        if (postOn1 == None):
            postOn = response.css('.newspage-main-info-meta-item3::text')[0]
            postOn1 = postOn.re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}')

            if not postOn1:
                postOn1 = postOn.re(r'\d+ 小')
                num = 3600
                if not postOn1:
                    postOn1 = postOn.re(r'\d+ 天')
                    num = 3600 * 24
                    if not postOn1:
                        postOn1 = postOn.re(r'\d+ 分')
                        num = 60

                postOn1 = postOn1[0]
                past_time = int(postOn1[:-2]) * num
                postOn1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()) - past_time))
            else:
                postOn1 = postOn1[0] + ':00'
        item['postOn'] = postOn1

        text = ''.join(response.css('.newspage-main-content p::text').extract())
        if (len(text) == 0):
            text = ''.join(response.css('.pcb *::text').extract())
        item['text'] = text

        return item
