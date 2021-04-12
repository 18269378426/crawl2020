# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import base64
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from random import choice
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.http import HtmlResponse
from selenium.webdriver.support.ui import WebDriverWait
import logging

class Crawl2020SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        # spider.logger.info('Spider opened: %s' % spider.name)
        pass


class DuobelProxyMiddleware(object):
    '''
    多贝代理  https://dobel.cn/
    https://github.com/dobelgit/dobelcloud/blob/master/Scrapy/middlewares.py
    '''

    def __init__(self) -> None:
        super().__init__()
        self.logger = logging.getLogger('DuobelProxyMiddleware' )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls() 
        return s

    def process_request(self, request, spider):
        # 设置代理服务器域名和端口，注意，具体的域名要依据据开通账号时分配的而定
        request.meta['proxy'] = "http://http-proxy-t1.dobel.cn:9180"
        # request.meta['proxy'] = "http://http-proxy-t3.dobel.cn:9180"

        # 设置账号密码
        proxy_user_pass = "WUCHANGB1EBQSR50:ao4yEBBC"
        # proxy_user_pass = "TESTXXXBBI3P8OO0:6xVlK1BB"
       # setup basic authentication for the proxy
        # For python3
        encoded_user_pass = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user_pass), "ascii")).decode("utf8")
        # For python2
        #encoded_user_pass = "Basic " + base64.b64encode(proxy_user_pass)
        request.headers['Proxy-Authorization'] = encoded_user_pass        
        self.logger.debug('set proxy for: %s' , spider)

 



class Crawl2020DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        # 配置成无头浏览器
        if hasattr(spider, 'dynamic') and spider.dynamic == True:
            if not hasattr(self, 'browser'):
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('blink-settings=imagesEnabled=false')
                chrome_options.add_argument('log-level=1')
                user_ag = choice(get_project_settings().get('USER_AGENT_CHOICES'))
                chrome_options.add_argument('user-agent=%s' % user_ag)
                self.browser = webdriver.Chrome(chrome_options=chrome_options)
            self.browser.get(url=request.url)
            try:
                WebDriverWait(self.browser, 30).until(lambda s: s.execute_script("return jQuery.active == 0"))
            except:
                pass
            return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf8", request=request)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        # spider.logger.info('Spider opened: %s' % spider.name)
        pass

    def spider_closed(self, spider):
        if hasattr(spider, 'dynamic') and spider.dynamic == True:
            self.browser.quit()
        pass


class RotateUserAgentMiddleware(object):
    """Rotate user-agent for each request."""

    def __init__(self, user_agents):
        self.enabled = False
        self.user_agents = user_agents

    @classmethod
    def from_crawler(cls, crawler):
        user_agents = crawler.settings.get('USER_AGENT_CHOICES', [])

        if not user_agents:
            raise NotConfigured("USER_AGENT_CHOICES not set or empty")

        return cls(user_agents)

    def process_request(self, request, spider):
        request.headers['USER-AGENT'] = choice(self.user_agents)
