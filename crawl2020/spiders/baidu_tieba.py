import logging
import scrapy
from datetime import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..baseSpider import BaseSpider
import re

class BaiduTiebaSpider(BaseSpider):
    name = 'baidu_tieba'
    source_name = '百度贴吧'
    allowed_domains = ['tieba.baidu.com']
    custom_settings = {
        'DOWNLOAD_DELAY': 10,
    }
    start_urls = ['https://tieba.baidu.com/f?kw=广西大学',
'https://tieba.baidu.com/f?kw=广西师范大学',
'https://tieba.baidu.com/f?kw=广西医科大学',
'https://tieba.baidu.com/f?kw=广西民族大学',
'https://tieba.baidu.com/f?kw=桂林电子科技大学',
'https://tieba.baidu.com/f?kw=桂林理工大学',
'https://tieba.baidu.com/f?kw=广西中医药大学',
'https://tieba.baidu.com/f?kw=广西科技大学',
'https://tieba.baidu.com/f?kw=南宁师范大学',
'https://tieba.baidu.com/f?kw=北部湾大学',
'https://tieba.baidu.com/f?kw=广西艺术学院',
'https://tieba.baidu.com/f?kw=桂林医学院',
'https://tieba.baidu.com/f?kw=右江民族医学院',
'https://tieba.baidu.com/f?kw=玉林师范学院',
'https://tieba.baidu.com/f?kw=河池学院',
'https://tieba.baidu.com/f?kw=广西财经学院',
'https://tieba.baidu.com/f?kw=梧州学院',
'https://tieba.baidu.com/f?kw=贺州学院',
'https://tieba.baidu.com/f?kw=百色学院',
'https://tieba.baidu.com/f?kw=广西民族师范学院',
'https://tieba.baidu.com/f?kw=桂林航天工业学院',
'https://tieba.baidu.com/f?kw=桂林旅游学院',
'https://tieba.baidu.com/f?kw=广西科技师范学院',
'https://tieba.baidu.com/f?kw=广西警察学院',
'https://tieba.baidu.com/f?kw=广西职业师范学院',
'https://tieba.baidu.com/f?kw=广西体育高等专科学校',
'https://tieba.baidu.com/f?kw=桂林师范高等专科学校',
'https://tieba.baidu.com/f?kw=广西幼儿师范高等专科学校',
'https://tieba.baidu.com/f?kw=广西职业技术学院',
'https://tieba.baidu.com/f?kw=南宁职业技术学院',
'https://tieba.baidu.com/f?kw=柳州职业技术学院',
'https://tieba.baidu.com/f?kw=广西机电职业技术学院',
'https://tieba.baidu.com/f?kw=广西水利电力职业技术学院',
'https://tieba.baidu.com/f?kw=广西交通职业技术学院',
'https://tieba.baidu.com/f?kw=广西建设职业技术学院',
'https://tieba.baidu.com/f?kw=广西农业职业技术学院',
'https://tieba.baidu.com/f?kw=广西生态工程职业技术学院',
'https://tieba.baidu.com/f?kw=广西国际商务职业技术学院',
'https://tieba.baidu.com/f?kw=广西工业职业技术学院',
'https://tieba.baidu.com/f?kw=广西经贸职业技术学院',
'https://tieba.baidu.com/f?kw=广西电力职业技术学院',
'https://tieba.baidu.com/f?kw=广西工商职业技术学院',
'https://tieba.baidu.com/f?kw=广西卫生职业技术学院',
'https://tieba.baidu.com/f?kw=柳州铁道职业技术学院',
'https://tieba.baidu.com/f?kw=广西现代职业技术学院',
'https://tieba.baidu.com/f?kw=北海职业学院',
'https://tieba.baidu.com/f?kw=柳州城市职业学院',
'https://tieba.baidu.com/f?kw=百色职业学院',
'https://tieba.baidu.com/f?kw=梧州职业学院',
'https://tieba.baidu.com/f?kw=广西金融职业技术学院',
'https://tieba.baidu.com/f?kw=广西安全工程职业技术学院',
'https://tieba.baidu.com/f?kw=广西自然资源职业技术学院',
'https://tieba.baidu.com/f?kw=崇左幼儿师范高等专科学校',
'https://tieba.baidu.com/f?kw=广西大学行健文理学院',
'https://tieba.baidu.com/f?kw=广西师范大学漓江学院',
'https://tieba.baidu.com/f?kw=广西民族大学相思湖学院',
'https://tieba.baidu.com/f?kw=桂林电子科技大学信息科技学院',
'https://tieba.baidu.com/f?kw=桂林理工大学博文管理学院',
'https://tieba.baidu.com/f?kw=广西中医药大学赛恩斯新医药学院',
'https://tieba.baidu.com/f?kw=柳州工学院',
'https://tieba.baidu.com/f?kw=南宁师范大学师园学院',
'https://tieba.baidu.com/f?kw=北京航天航空大学北海学院',
'https://tieba.baidu.com/f?kw=广西外国语学院',
'https://tieba.baidu.com/f?kw=南宁学院',
'https://tieba.baidu.com/f?kw=北海艺术设计学院',
'https://tieba.baidu.com/f?kw=广西城市职业大学',
'https://tieba.baidu.com/f?kw=广西演艺职业学院',
'https://tieba.baidu.com/f?kw=桂林山水职业学院',
'https://tieba.baidu.com/f?kw=广西英华国际职业学院',
'https://tieba.baidu.com/f?kw=广西工程职业学院',
'https://tieba.baidu.com/f?kw=广西理工职业技术学院',
'https://tieba.baidu.com/f?kw=广西经济职业学院',
'https://tieba.baidu.com/f?kw=广西科技职业学院',
'https://tieba.baidu.com/f?kw=广西培贤国际职业学院',
'https://tieba.baidu.com/f?kw=玉柴职业技术学院',
'https://tieba.baidu.com/f?kw=广西蓝天航空职业学院',
'https://tieba.baidu.com/f?kw=广西中远职业技术学院',
'https://tieba.baidu.com/f?kw=桂林生命与健康职业技术学院',
'https://tieba.baidu.com/f?kw=广西开放大学',
'https://tieba.baidu.com/f?kw=广西教育学院',
'https://tieba.baidu.com/f?kw=广西政法管理干部学院',
'https://tieba.baidu.com/f?kw=桂林市职工大学',
'https://tieba.baidu.com/f?kw=梧州医学高等专科学校',
'https://tieba.baidu.com/f?kw=广西物流职业技术学院',
'https://tieba.baidu.com/f?kw=钦州幼儿师范高等专科学校',
'https://tieba.baidu.com/f?kw=广西制造工程职业技术学院',]
    spider_tags = ['广西', '贴吧', '高校']

    # rules = [
    #     Rule(LinkExtractor(allow=(r'p/\d+',), deny=('pid=', 'pn=')),callback='parse_item', follow=False)]

# {'title': '疫情一来什么生意都难做，实体店酒店ktv酒吧粉店关门，害是有"',
#   'title_href': 'https://tieba.baidu.com/p/7192631051',
#   'author_name': '老干妈302',
#   'author_id': '552151095',
#   'author_home': 'https://tieba.baidu.com/home/main/?un=%E8%80%81%E5%B9%B2%E5%A6%88302&ie=utf-8&id=tb.1.4cd40f6d.JEi4-8MUGN1MQQlDKDXtgA&fr=frs',
#   'content': '\n            疫情一来什么生意都难做，实体店酒店ktv酒吧粉店关门，害是有份稳定工作稳\n        ',
#   'image': []}

    def _parse(self, response, **kwargs):
        results = re.findall(r'<a rel="noreferrer" href="(/p/\d+)" title="(\S+)"', response.body.decode())
        for url,title in results:
            yield scrapy.Request('https://tieba.baidu.com' +url, callback=self.parse_item)
        # print( response.text)
        # items = PageKeyInfo(response.body.decode()).run()
        # print('parse:%s',items)
        # for o in items:
        #     if 'title_href' in o and o['title_href']:
        #         yield scrapy.Request(o['title_href'], callback=self.parse_item)

    def parse_item(self, response):
         
        item = self.createItem(response)
        item['postOn'] = ''
        item['postBy'] = response.css('.d_name ::text').extract()[1]
        item['title'] =  response.css('.core_title_txt ::text').extract_first()
        item['taskName'] = response.css('.p_author_face img::attr(src)').extract_first()
        item['text'] =  '\n'.join([x.strip() for x in response.xpath('//div[@id and contains(@id,"post_content_")]').css('*::text').extract()])
        if len(item['title']) == 0:
            self.error('error: 获取不到帖子标题,' + response.url)
            return None
        return item
 
# class PageKeyInfo():
#     """传入的参数为response产生的原始字符串"""
#     def __init__(self, html_str):
#         """初始化参数"""
#         self.html_str = html_str

#     def __info_str(self, html_str):
#         """将传入的html_str分解，提取有用的内容"""
#         html_ = re.findall(r'<code class=\"pagelet_html\" id=\"pagelet_html_frs-list/pagelet/thread_list\" style=\"display:none;\">(.*?)</code>', html_str, re.S)[0]
#         return html_

#     def __get_usefulinfo_by_one(self,ul_one):
#         one_tiezi_info = dict()
#         # 获取标题和地址
#         title_and_href = re.findall(r'j_th_tit ">.*?<a rel="noreferrer" href="(.*?)" title="(.*?) target="_blank"', ul_one, re.S)
#         title_and_href = title_and_href[0] if len(title_and_href) > 0 else None
#         if title_and_href:
#             title_href_ = "https://tieba.baidu.com"+title_and_href[0]
#             title_ = title_and_href[1]
#         else:
#             title_href_ = None
#             title_ = None
#         # 获取作者和作者id
#         author_name = re.findall(r'<span class="tb_icon_author ".*?title="主题作者: (.*?)"', ul_one, re.S)
#         author_name = author_name[0] if len(author_name) > 0 else None
#         author_id = re.findall(r'title="主题作者.*?".*?data-field=\'{&quot;user_id&quot;:(.*?)}\' >', ul_one, re.S)
#         author_id = author_id[0] if len(author_id) > 0 else None
#         author_home = re.findall(r'class="frs-author-name j_user_card " href="(.*?)" target="_blank">', ul_one, re.S)
#         author_home = "https://tieba.baidu.com" + author_home[0] if len(author_home) > 0 else None
#         # 取内容
#         content = re.findall(r'<div class="threadlist_abs threadlist_abs_onlyline ">(.*?)</div>', ul_one, re.S)
#         content = content[0] if len(content) > 0 else None
#         image = re.findall(r'bpic="(.*?)" class="threadlist_pic j_m_pic', ul_one, re.S)
#         # 将数据存放在字典中
#         one_tiezi_info["title"] = title_
#         one_tiezi_info["title_href"] = title_href_
#         one_tiezi_info["author_name"] = author_name
#         one_tiezi_info["author_id"] = author_id
#         one_tiezi_info['author_home'] = author_home
#         one_tiezi_info['content'] = content
#         one_tiezi_info['image'] = image
#         return one_tiezi_info

#     def __ul_content(self,html_):
#         # 获取当前主题页的所有列表
#         ul_content_list = re.findall(r'li class=\" j_thread_list clearfix\"(.*?)<li class=\" j_thread_list clearfix\"', html_, re.S)
#         return ul_content_list

#     def __get_content(self,html_):
#         item_list = list()
#         # 获取包含所有单块帖子的列表
#         ul_content_list = self.__ul_content(html_)
#         for ul_one in ul_content_list:
#             item = self.__get_usefulinfo_by_one(ul_one)
#             item_list.append(item)
#         return item_list

#     def run(self):
#         # 处理字符串
#         __html_ = self.__info_str(self.html_str)
#         # 处理关键字段
#         __item_list = self.__get_content(__html_)
#         return __item_list        