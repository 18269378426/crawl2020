import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisSpider #导入RedisSpider


class BbsHepu123Spider(BaseSpider):
    name = 'bbs_hepu123'
    source_name = '合浦123论坛'
    allowed_domains = ['bbs.hepu123.com']
    spider_tags = ['广西', '北海', '合浦', '论坛']
    start_urls = [
        'http://bbs.hepu123.com/forum-2-1.html'
    ]
    rules = [Rule(LinkExtractor(allow=(r'forum.php\?mod=viewthread&tid=\d+&extra=page%3D1')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.title-cont a span::text').extract_first()

        item['taskName'] = response.css('.a-img img::attr(src)').extract_first()

        item['postBy'] = response.css('.name::attr(title)').extract_first()

        postOn = response.css('.u-add .z::text').re(r'\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}:\d{2}')
        if postOn:
            item['postOn'] = postOn[0]
        else:
            item['postOn'] = response.css('.u-add .z span::attr(title)').extract_first()

        item['text'] = ''.join(response.css('.t_fsz *::text').extract())

        return item
