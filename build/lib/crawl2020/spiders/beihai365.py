import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class Beihai365Spider(BaseSpider):
    name = 'beihai365'
    source_name = '北海365论坛'
    allowed_domains = ['kj.beihai365.com', 'www.beihai365.com']
    spider_tags = ['广西', '北海', '论坛']
    start_urls = [
        'http://kj.beihai365.com/',
        'http://www.beihai365.com/thread.php?fid=231',
        'http://www.beihai365.com/thread.php?fid=762'
    ]
    rules = [Rule(LinkExtractor(allow=(r'read.php\?tid=\d+$')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('#subject_::text').extract_first()

        taskName = response.css('.userCard.face_img img::attr(src)').extract_first()
        if "http" not in taskName:
            taskName = "http://www.beihai365.com/" + taskName
        item['taskName'] = taskName

        item['postBy'] = response.css('.r_name a::text').extract_first()

        item['postOn'] = response.css('.title_bottom_t span::attr(title)').extract_first() + ':00'

        item['text'] = ''.join(response.css('.f16.hehe2 *::text').extract())

        return item
