from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import logging
from datetime import datetime


class PbttSpider(BaseSpider):
    name = 'pbtt'

    source_name = '浦北天天网'
    spider_tags = ['广西', '浦北', '论坛']
    allowed_domains = ['www.pbtt.net']
    start_urls = ['https://www.pbtt.net/forum-2-1.html',
                  'https://www.pbtt.net/forum-39-1.html']
    rules = [Rule(LinkExtractor(allow=(r'thread-\d+-1-1.html')), callback='parse_item', follow=False)]

    def parse_item(self, response):
        if '提示信息' in response.css('title::text').extract_first():
            self.log('指定的主题不存在或已被删除或正在被审核：' + response.url, logging.INFO)
            super().dot_crawl_url(response.url)
            return None
        item = self.createItem(response)

        item['title'] = ' '.join(response.css('#thread_subject::text').extract())

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        if (len(item['title']) == 0):
            self.error('error: 获取不到帖子标题,' + response.url, logging.DEBUG)
            return None

        item['postBy'] = response.css('div.authi>a::text').extract_first()

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

        item['text'] = '\n'.join([y for y in [x.strip() for x in response.css('td.t_f *::text').extract()] if y != ''])

        return item
