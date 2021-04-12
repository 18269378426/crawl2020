
from scrapy.utils.project import get_project_settings
from elasticsearch import Elasticsearch
import logging
from scrapy.dupefilters import BaseDupeFilter
from . import elasticHelper
from pybloom_live import ScalableBloomFilter
from pydispatch import dispatcher
from . import mysignals

IGNORE_URL=[]

class ElasticSearchDumpFilter(BaseDupeFilter):
    """
    docstring
    """

    def __init__(self, settings, es_settings):
        self.es = Elasticsearch(**es_settings)
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        # self.ignore_urs=ScalableBloomFilter(initial_capacity=100, error_rate=0.001, mode=ScalableBloomFilter.LARGE_SET_GROWTH)
        self.ignore_urs=IGNORE_URL
        dispatcher.connect(self.signal_ignore_url, signal=mysignals.signal_ignore_url)
 
    @classmethod
    def from_settings(cls, settings):
        es_settings = elasticHelper.get_es_settings(settings)
        return cls(settings, es_settings)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def signal_ignore_url(self,url):
        self.ignore_urs.append(url)

        
    def request_seen(self, request):
        url = request.url
        if url in self.ignore_urs:
            self.logger.debug(f'ignore_urs: {url}' )
            return True

        exists = elasticHelper.doc_exists(self.settings, self.es, url)
        if exists:
            self.ignore_urs.append(url)
            # dispatcher.send(mysignals.signal_ignore_url, None, url)
        return exists

    def open(self):
        pass

    def close(self, reason):
        pass

    def clear(self):
        self.es.close()
        pass
