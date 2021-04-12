# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from kafka import KafkaProducer, producer
from itemadapter import ItemAdapter
from datetime import datetime
from elasticsearch import Elasticsearch, helpers

import logging
import types
import re
import pytz

from . import elasticHelper

tz = pytz.timezone('Asia/Shanghai')


class Crawl2020Pipeline:
    def process_item(self, item, spider):
        return item


class InvalidSettingsException(Exception):
    pass


class ConvertPostOnPipeline(object):

    def __init__(self) -> None:
        self.logger = logging.getLogger('ConvertPostOnPipeline')

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            if 'postOn' in item and item['postOn'] and isinstance(item['postOn'], str):
                try:
                    item['postOn'] = datetime.strptime(
                        item['postOn'].strip(), '%Y-%m-%d %H:%M:%S').astimezone(tz)
                except:
                    self.logger.error('error postOn: %s,%s ', item['postOn'], item['url'])
                    item['postOn'] = datetime.now(tz=tz)
            elif 'postOn' in item and item['postOn'] and isinstance(item['postOn'], datetime):
                item['postOn'] = item['postOn'].astimezone(tz=tz)
            else:
                item['postOn'] = datetime.now(tz=tz)

            return item


class ClearTextPipeline(object):
    pattern = re.compile(r"[\x00-\x1f\x7f ]")

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            if item['text']:
                item['text'] = self.clearText(item)
            item['title'] = (item['title'] or '').strip()

            return item

    def clearText(self, item):

        text = '\n'.join(item['text']) if isinstance(
            item, types.GeneratorType) or isinstance(item, list) else item['text']
        # text.replace('\t', '').replace('\n', '').replace('\r', '').replace(' ','')
        text = re.sub(self.pattern, '', text)
        return text


class KafkaPipeline(object):
    settings = None
    producer = None
    topic = 'bbs'

    def __init__(self):
        self.logger = logging.getLogger('KafkaPipeline')

    def __del__(self):
        self.producer.close()

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        ext.producer = KafkaProducer(bootstrap_servers=['localhost:9092'], compression_type='gzip', value_serializer=lambda v: json.dumps(dict(v), default=str).encode('utf-8'))
        return ext

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            self.send_item(item)
            return item

    def send_item(self, item):
        self.logger.info('send item {spider},{title},{url}'.format(**{
            'spider': item['spider'],
            'title': item['title'],
            'url': item['url'],
        }))
        self.producer.send(self.topic, value=item)

    def close_spider(self, spider):
        pass


class ElasticSearchPipeline(object):
    '''https://github.com/jayzeng/scrapy-elasticsearch'''

    settings = None
    es = None
    items_buffer = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    @classmethod
    def init_es_client(cls, crawler_settings):
        es_settings = dict()
        es_settings['hosts'] = crawler_settings.get(
            'ELASTICSEARCH_SERVERS', 'localhost:9200')
        es_settings['timeout'] = crawler_settings.get(
            'ELASTICSEARCH_TIMEOUT', 60)

        es = Elasticsearch(**es_settings)
        return es

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        ext.settings = crawler.settings

        ext.es = cls.init_es_client(crawler.settings)
        return ext

    def index_item(self, item):

        index_action = {
            '_index': elasticHelper.get_index_name(self.settings),
            '_source': dict(item)
        }

        index_action['_id'] = elasticHelper.get_doc_id(item['url'])

        self.items_buffer.append(index_action)

        if len(self.items_buffer) >= self.settings.get('ELASTICSEARCH_BUFFER_LENGTH', 10):
            self.send_items()
            self.items_buffer = []

    def send_items(self):
        helpers.bulk(self.es, self.items_buffer)

    def process_item(self, item, spider):
        if isinstance(item, types.GeneratorType) or isinstance(item, list):
            for each in item:
                self.process_item(each, spider)
        else:
            self.index_item(item)
            self.logger.debug('Item sent to Elastic Search %s' %
                              self.settings['ELASTICSEARCH_INDEX'])
            return item

    def close_spider(self, spider):
        if len(self.items_buffer):
            self.send_items()
