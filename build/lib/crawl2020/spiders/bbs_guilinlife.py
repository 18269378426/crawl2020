import logging
import scrapy
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..baseSpider import BaseSpider


class BbsGuilinlifeSpider(BaseSpider):
    name = 'bbs_guilinlife'
    source_name = '桂林生活网论坛'
    allowed_domains = ['bbs.guilinlife.com']
    start_urls = ['http://bbs.guilinlife.com/forum.php?mod=forumdisplay&fid=27',
                  'http://bbs.guilinlife.com/forum-27-1.html',
                  'http://bbs.guilinlife.com/forum-61-1.html']
    spider_tags = ['广西', '桂林', '论坛']

    rules = [
        Rule(LinkExtractor(allow=('thread\-(\d+)\-1\-1.html', 'forum.php\?mod=viewthread&tid=\d+&extra=page%3D1$')),
             callback='parse_item', follow=False)]

    def parse_item(self, response):
        if '提示信息' in response.css('title::text').extract_first():
            self.log('指定的主题不存在或已被删除或正在被审核：' + response.url, logging.INFO)
            self.dot_crawl_url(response.url)
            return None

        item = self.createItem(response)



        item['title'] = ' '.join(response.css('#thread_subject *::text').extract())
        if (len(item['title']) == 0):
            self.error('error: 获取不到帖子标题,' + response.url, logging.DEBUG)
            return None

        item['taskName'] = response.css('.avtm img::attr(src)').extract_first()

        item['postBy'] = response.css('a.xw1::text').extract_first()

        # 发贴时间，有二种格式： xxxx小时前 或 具体的日期时间

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
