import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import re

class LiuyanPeopleSpider(BaseSpider):
    name = 'liuyan_people'
    source_name = '人民网留言'
    allowed_domains = ['liuyan.people.com.cn']
    spider_tags = ['广西', '问政']
    start_urls=[]
 
    headers = {"Content-Type": "application/x-www-form-urlencoded",
                "Referer": "http://liuyan.people.com.cn/threads/list?fid=3561",
                    "Origin": "http://liuyan.people.com.cn"
                }
    
    def start_requests(self):

        # fids = [1259, 1260,]
        # 所有留言本ID
        fids = [1259, 1260, 1261, 1262, 1263, 1264, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1274, 1275, 1276, 1277, 1278, 1279, 1280, 1281, 1282, 1283, 1284, 1559, 1560, 1590, 1591, 3561, 3562, 3563, 3564, 3565, 3566, 3568, 3569, 3570, 3571, 3572, 3573, 3574, 3575, 3576, 3577, 3578, 3579, 3580, 3581, 3582, 3583, 3584, 3585, 3586, 3587, 3588, 3589, 3590, 3591, 3592, 3593, 3601, 3602, 3603, 3604, 3605, 3606, 3607, 3608, 3609, 3610, 3611, 3612, 3613, 3614, 3615, 3618, 3619, 3620, 3621, 3622, 3623, 3624, 3625, 3626, 3627, 3628, 3629, 3630, 3631, 3632, 3633, 3634, 3635, 3636, 3637, 3638, 3639, 3640, 3641, 3642, 3643, 3644, 3645, 3646, 3647, 3648, 3649, 3650, 3651, 3652, 3653, 3654, 3655, 3656, 3657, 3658, 3659, 3660, 3661, 3662, 3663, 3664, 3665, 4389, 4390, 4391, 4392, 4393, 4394, 4395, 4465, 4466, 4467, 4468, 4469, 4470, 4471, 4687, 4729, 5102]

        for fid in fids:
            yield scrapy.http.FormRequest(url='http://liuyan.people.com.cn/threads/queryThreadsList',
                                          formdata={"fid": f'{fid}', "lastItem": "0"},
                                          method='POST',
                                          headers=self.headers,
                                          callback=self.queryThreadsList
                                          )

    def queryThreadsList(self, response):
        r = response.json()
        # self.logger.info('queryThreadsList .url: %s,%s,%s', response.url, r['result'], len(r['responseData']))
        for o in r['responseData']:
            yield scrapy.http.FormRequest(url=f'http://liuyan.people.com.cn/threads/content?tid={o["tid"]}', meta={'data': o},callback=self.parse_item)

    def parse_item(self, response):        
        item = self.createItem(response)
        item['title'] = response.css('.context-title-text::text').extract_first()
        item['taskName'] = "http://liuyan.people.com.cn/static/www/images/logo2.png"
        postBy = response.css('h3.grey2 span::text').extract_first()
        item['postBy'] =  re.sub(r'\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}', '', postBy).strip()
        item['postOn'] = response.css('h3.grey2 span::text').re(r'\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0] + ':00'
        item['text'] = ''.join(response.css('.content *::text').extract())
        self.logger.info(f'rsult: {item["title"]},{response.url}')
        return item

                                          
# class LiuyanPeopleSpider(BaseSpider):
#     name = 'liuyan_people'
#     source_name = '人民网留言'
#     allowed_domains = ['liuyan.people.com.cn']
#     spider_tags = ['广西', '问政']
#     start_urls = [
#         'http://liuyan.people.com.cn/forum/list?fid=31'
#     ]
#     rules = [
#         Rule(LinkExtractor(allow=(r'/forum/list\?fid=\d+'), restrict_css=('.district_box04')), follow=False, callback='forum_list'),
#         # Rule(LinkExtractor(allow=(r'/threads/list\?fid=\d+')), follow=True, callback='parse_list'),
#         Rule(LinkExtractor(allow=(r'/threads/content\?tid=\d+')), callback='parse_item', follow=False),

#     ]

#     # dynamic = True

#     def forum_list(self, response):
#         # self.logger.info('forum_list.url: %s', response.url)
#         forums = response.css('a.count-limit::attr(href)').extract()

#         for f in forums:
#             self.logger.info('forum_list : %s', f)
#             id = f.split('fid=')[-1]
#             headers = {"Content-Type": "application/x-www-form-urlencoded",
#                        "Referer": "http://liuyan.people.com.cn/threads/list?fid=3561",
#                        "Origin": "http://liuyan.people.com.cn"
#                        }
#             # return scrapy.http.JsonRequest(url='http://liuyan.people.com.cn/threads/queryThreadsList', data={"fid" :  id, "lastItem" : 0},callback = self.queryThreadsList)
#             yield scrapy.http.FormRequest(url='http://liuyan.people.com.cn/threads/queryThreadsList',
#                                           formdata={"fid": f'{id}', "lastItem": "0"},
#                                           method='POST',
#                                           headers=headers,
#                                           callback=self.queryThreadsList
#                                           )
#         msg_links = response.css('a.message_index::attr(href)').extract()
#         for link in msg_links:            
#             yield scrapy.http.FormRequest(url=f'http://liuyan.people.com.cn{link}' )
# # {'tid': 9024562, 'userId': 3897827,
# # 'fid': 3611, 'typeId': 2, 'domainId': 7,
# # 'topicId': 0, 'nickName':
# # '陈***', 'subject': '新兴路成为混凝土公司专用道路面损严重',
# # 'content': '新兴路自2008年修建完成就没有停止过路面切割重复施工，2019年打通新兴北路后，混凝土公司以及周边建设工地的重卡车运沙运石就每天在此路通行。几十上百吨重卡车每次负重经过沿线都居民都感到地动山摇，每天...',
# # 'dateline': 1610983347, 'ip': '124.227.4.*',
# # 'stateInfo': '待回复', 'traceInfo': '待回复',
# # 'processInfo': '未交办', 'hasReported': 0,
# # 'favNum': 0, 'forumName': '灵山县委书记',
# # 'typeName': '投诉', 'domainName': '城建',
# # 'sourceName': 'PC浏览器', 'answerId': None,
# # 'answerContent': None, 'answerDateline': None,
# # 'answerOrganization': None, 'userType': 0,
# # 'threadState': 1, 'publicAttachment': 1,
# # 'userFavStatus': 0, 'grade': None, 'gradeLevel': None,
# # 'gradeManner': None, 'gradeSpeed': None, 'trashRecheckState': 0,
# # 'attachment': 1, 'threadsCheckTime': 1611053337, 'from': ' 广西壮族自治区 钦州市', 'shisiwu': False}

#     def queryThreadsList(self, response):
#         r = response.json()
#         # self.logger.info('queryThreadsList .url: %s,%s,%s', response.url, r['result'], len(r['responseData']))
#         for o in r['responseData']:
#             yield scrapy.http.FormRequest(url=f'http://liuyan.people.com.cn/threads/content?tid={o["tid"]}', meta={'data': o},callback=self.parse_item)

#     def parse_item(self, response):
        
#         item = self.createItem(response)
#         item['title'] = response.css('.context-title-text::text').extract_first()
#         postBy = response.css('h3.grey2 span::text').extract_first()
#         item['postBy'] = re.sub(r'\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}', '', postBy)
#         item['postOn'] = response.css('h3.grey2 span::text').re(r'\d{4}-\d{1,2}-\d{1,2} \d{2}:\d{2}')[0] + ':00'
#         item['text'] = ''.join(response.css('.content *::text').extract())
#         self.logger.info(f'rsult: {item["title"]},{response.url}')
#         return item




## 临时，用于获取所有 fid
# class LiuyanPeopleSpider(BaseSpider):
#     name = 'liuyan_people_temp'
#     source_name = '人民网留言'
#     allowed_domains = ['liuyan.people.com.cn']
#     spider_tags = ['广西', '问政']
#     start_urls = [
#         'http://liuyan.people.com.cn/forum/list?fid=31'
#     ]
#     rules = [
#         Rule(LinkExtractor(allow=(r'/forum/list\?fid=\d+'), restrict_css=('.district_box04')), follow=False, callback='forum_list'),
        
#     ]

#     # dynamic = True

#     def forum_list(self, response):
#         # r = response.xpath('//a[contains(@href, "thread")]').css('::attr(href)').extract()
#         arr=[ {'url':x.css('::attr(href)').extract_first(),"name":x.css('::text').extract_first()} for x in  response.xpath('//a[contains(@href, "/threads/list?fid=")]')]
#         self.logger.error('threads:%s',arr)