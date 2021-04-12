# import scrapy
# from ..baseSpider import BaseSpider
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule
# import logging
# from datetime import datetime
#
# class WygxSpider(BaseSpider):
#     name = 'wygx'
#     source_name = '网易广西'
#     allowed_domains = ['gx.news.163.com', 'www.163.com', 'dy.163.com']
#     spider_tags = ['广西', '新闻']
#     start_urls = [
#         'https://gx.news.163.com/',
#         'http://gx.news.163.com/guilin/'
#     ]
#     dynamic = True
#     rules = [Rule(LinkExtractor(allow=(r'http://dy.163.com/v2/article/detail/\w+.html', r'http://gx.news.163.com/\d+/\d+/\d+/\w+.html')), callback='parse_item', follow=False)
#     ]
#
#     def parse_item(self, response):
#
#         if not response.css('.post_title::text').extract_first():
#             self.log("页面错误："+response.url, logging.INFO)
#             return None
#         item = self.createItem(response)
#
#         item['title'] = response.css('.post_title::text').extract_first()
#
#         item['taskName'] = response.css('.avtm img::attr(src)').extract_first()
#
#         item['postBy'] = response.css('.post_info::text').re('[^0-9]:(.+)')[0]
#
#         item['postOn'] = response.css('.post_info::text').re(r'\d{4}\-\d{1,2}\-\d{1,2} \d{2}:\d{2}:\d{2}')
#
#
#         item['text'] = ''.join(response.css('.post_body *::text').extract())
#
#         return item
