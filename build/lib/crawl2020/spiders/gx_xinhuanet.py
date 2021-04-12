import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule


class GxXinhuanetSpider(BaseSpider):
    name = 'gx_xinhuanet'
    source_name = '新华网（广西频道）'
    allowed_domains = ['www.gx.xinhuanet.com']
    spider_tags = ['广西', '新华']
    start_urls = [
        'http://www.gx.xinhuanet.com',
        'http://www.gx.xinhuanet.com/newscenter/yw.htm'

    ]
    rules = [Rule(LinkExtractor(allow=(r'http://www.gx.xinhuanet.com/newscenter/\d+-\d+/\d+/c_\d+.htm')), callback='parse_item', follow=False)]

    def parse_item(self, response):

        item = self.createItem(response)

        title = response.css('.h-title::text').extract_first()
        if title:
            item['title'] = title

            item['taskName'] = 'http://www.newsimg.cn/xl2017/images/net_logo.png'

            item['postBy'] = response.css('#source a::text').extract_first()

            item['postOn'] = response.css('.h-time::text').extract_first().strip()

            item['text'] = ''.join(response.css('#p-detail *::text').extract())
        else:
            item['title'] = response.css('#title::text').extract_first()

            item['taskName'] = 'http://www.newsimg.cn/xl2017/images/net_logo.png'

            item['postBy'] = response.css('#source::text').extract_first()

            item['postOn'] = response.css('#pubtime::text').extract_first().replace('年', '-').replace('月', '-').replace('日', '')

            item['text'] = ''.join(response.css('#content *::text').extract())
            all_page = response.xpath('//div[@id="div_currpage"]/a[@class="page-Article"]/@href').extract()

            for page in all_page:
                scrapy.Request(url=page, callback=self.parse_page, meta={'item': item})

        return item

    def parse_page(self, response):
        item = response.meta['item']
        item['text'] = item['text'] + ''.join(response.css('#content *::text').extract())
