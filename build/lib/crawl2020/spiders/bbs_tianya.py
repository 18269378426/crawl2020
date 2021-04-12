import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class BbsTianyaSpider(BaseSpider):
    name = 'bbs_tianya'
    source_name = '天涯社区'
    allowed_domains = ['bbs.tianya.cn']
    spider_tags = ['广西', '论坛']

    start_urls = [
        'http://gx.tianya.cn/',
        'http://bbs.tianya.cn/list-79-1.shtml',
        'http://bbs.tianya.cn/list-990-1.shtml',
        'http://bbs.tianya.cn/list-689-1.shtml',
        'http://bbs.tianya.cn/list-1029-1.shtml',
        'http://bbs.tianya.cn/list-325-1.shtml',
        'http://bbs.tianya.cn/list-326-1.shtml',
        'http://bbs.tianya.cn/list-327-1.shtml',
        'http://bbs.tianya.cn/list-5219-1.shtml',
        'http://bbs.tianya.cn/list-828-1.shtml',
        'http://bbs.tianya.cn/list-law-1.shtml'
    ]
    rules = [Rule(LinkExtractor(allow=(r'post-\d+-\d+-\d+.shtml', r'http://bbs.tianya.cn/post-\d+-\d+-\d+.shtml')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.s_title>span::text').extract_first()

        item['taskName'] = 'https://static.tianyaui.com/global/bbs/web/static/images/nav_top_logo_35.png'

        item['postBy'] = response.css('.js-vip-check::text').extract_first()

        item['postOn'] = response.css('.atl-info>span::text')[1].re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')[0]

        item['text'] = ''.join(response.css('.bbs-content::text').extract())

        return item
