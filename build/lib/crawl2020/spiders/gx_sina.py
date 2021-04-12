# import scrapy
# from ..baseSpider import BaseSpider
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import Rule
# import logging
# from datetime import datetime
#
# class GxSinaSpider(BaseSpider):
#     name = 'gx_sina'
#     source_name = '新浪广西'
#     allowed_domains = ['gx.sina.com.cn']
#     spider_tags = ['广西', '新闻']
#     start_urls = [
#         'http://gx.sina.com.cn/news/gx/list.shtml',
#         'http://gx.sina.com.cn/news/gx/list.shtml',
#         'http://gx.sina.com.cn/news/sh/list.shtml',
#         'http://gx.sina.com.cn/news/nn/list.shtml',
#         'http://gx.sina.com.cn/news/minsheng/list.shtml'
#
#     ]
#     dynamic = True
#     rules = [Rule(LinkExtractor(allow=(r'http://gx.sina.com.cn/news/gx/\d+-\d+-\d+/detail-\w+.shtml')), callback='parse_item', follow=False)
#     ]
#
#     def parse_item(self, response):
#
#         item = self.createItem(response)
#
#         item['title'] = response.css('.article-header h1::text').extract_first()
#
#         item['taskName'] = "http://n.sinaimg.cn/jx/images/sinalogo-nav.png?v=4"
#
#         item['postBy'] = '新浪广西' #没有作者
#
#         item['postOn'] = response.css('.source-time::text')
#
#
#         item['text'] = ''.join(response.css('.article-body *::text').extract())
#
#         return item