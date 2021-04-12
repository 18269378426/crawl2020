import scrapy
from ..baseSpider import BaseSpider
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
import json
class ToutiaoSpider(BaseSpider):
    name = 'toutiao'
    source_name = '头条号'
    allowed_domains = ['www.toutiao.com']
    spider_tags = ['广西', '新闻']
    start_urls = [
        'https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAAin-7bBv5ppySj8x4gebz8kge7rzqtH03RNQzoYMOXSo&max_behot_time=0&_signature=_02B4Z6wo00d013ydBSQAAIDAzGzp7vkGcit8uAGAAL8utcghrq-D8eo6VAr69LBGe8mNXcAp9JrHBQtZo4zb4LIQrQdLg0rf8RTYmQ741n.CCqVEhFW1z5UX9ELBG.AtZ3cC.NeYByeNvGSUf9',
        'https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAAfRCkl8qCBxOB1PbMDAgVVAFbHfmQ-806BAv4qpH7WI4&max_behot_time=0&_signature=_02B4Z6wo00f016jF31gAAIDAGDQzkzjNH3-o4NvAAIo9ww020vs8AUykcOA1QSaiDb1gdWcqvQb5LjN2k5am4olUwj9r6CUiKyeYMW0OZunqqOB-4cQd8.a-Kcw5mRgPxJO7ArPLDOiqgXQd09',
        'https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAADRkgBDdJpBqFULfPbe8bUcoqba80n-6ym71ofgeZ-ks&max_behot_time=0&_signature=_02B4Z6wo00f0119mrZgAAIDA75dBU4Ci8f9fQ6kAALfnfk8zDGUSgwvTBAbb-9936kKH-QEeDt8YrabrrFsbNb3Ucw-Rq6eY-dOgkY5ZJGzpXD6o2.Y0hk5j42yLdeBvqgRKQ30N5bCUqNXkcb',
        'https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAA4x6xZBxIaYnhFJ_G0cKUrSvrlDAetEmxYrAa04aXKkI&max_behot_time=0&_signature=_02B4Z6wo00d01nLeimAAAIDBwi9mqJGm2q5y-47AAPzBhBvdFY0fINh9B44FFTbL5TFoUFoM4ApQn5SQQKVojQXhPi1BH13pWOJBRpKA6OQ5ebRxNA2.iTmGHIZc2eJBl36XbvGGUhyAU3vSca',
        'https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAARnTuZ9N2DVRlbafa9TFnRRxd2ry5_rEEIfrfEjHVmbY&max_behot_time=0&_signature=_02B4Z6wo00f01rzhI6wAAIDBDBDPZ6RXLjK8xCcAAM9KjCxIQxMGQ65bNC2669QIyvYn3Kb7h8Pabi-XaE8GPe6hoLIRWk6pV0J4FWqpZFKVVbUOSiaGLOVuFFToURG7JTyiKK8RKa8p0vMv74',
        'https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAAWggDU5dKdmwSzXmzFZ0cx2ru3gT0_-Pr_2yVhV7Zedg&max_behot_time=0&_signature=_02B4Z6wo00f01MSqvaAAAIDDdFtRa4D9UCTEj7kAAFE0FgGtbYShcC1pRmpPOHfG6FP.euqkpGsACZCzcpofQ.hTXdhFS.cuOqpdahP4GANXpd4C6o.yQHObI9RsONCd4E4iwtrruaOsg6651d',

    ]
    # rules = [
    #     Rule(LinkExtractor(allow=(r'/item/\d+/')), callback='parse_item', follow=False),         
    # ]


    # dynamic = True
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={
                'dont_redirect': True
                },
                callback=self.parse_json)

    def parse_json(self, response):
        json_str = json.loads(response.text)
        for data in json_str['data']:
            url = 'https://www.toutiao.com/i' + data['group_id'] + '/'
            yield scrapy.Request(url, meta={
                'dont_redirect': True
                },callback=self.parse_item)
    def parse_item(self, response):

        item = self.createItem(response)

        item['title'] = response.css('.article-content h1::text').extract_first()

        item['taskName'] = "https://s3a.pstatp.com/toutiao/resource/ntoutiao_web/static/image/other/report_logo_15cc24e.png"

        item['postBy'] = response.css('.article-meta span::text').extract_first()

        item['postOn'] = response.css('.article-meta span::text')[1].get()

        item['text'] = ''.join(response.css('.syl-page-article *::text').extract())

        return item
