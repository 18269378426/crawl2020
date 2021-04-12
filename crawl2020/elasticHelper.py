
from datetime import datetime
import hashlib
from six import string_types
import logging

logger = logging.getLogger(__name__)

def get_index_name(settings):

    index_name = settings['ELASTICSEARCH_INDEX']
    index_suffix_format = settings.get(
        'ELASTICSEARCH_INDEX_DATE_FORMAT', None)

    dt = datetime.now()
    index_name += "-" + datetime.strftime(dt, index_suffix_format)

    return index_name


def get_doc_id(url):
    item_id = hashlib.sha1(url.encode('utf-8')).hexdigest()
    return item_id


def get_es_settings(settings):
    es_timeout = settings.get('ELASTICSEARCH_TIMEOUT', 60)

    es_servers = settings.get(
        'ELASTICSEARCH_SERVERS', 'localhost:9200')
    es_servers = es_servers if isinstance(
        es_servers, list) else [es_servers]

    es_settings = dict()
    es_settings['hosts'] = es_servers
    es_settings['timeout'] = es_timeout
    return es_settings


def doc_exists(settings, es, url):
    id = get_doc_id(url)
    dsl = {
        "query": {
            "match": {
                "_id": id
            }
        }, "fields": ["_id", "url"], "_source": False
    }

    result = es.search(index=get_index_name(settings),   body=dsl)
    # self.logger.info('search result: %s', result)
    is_time_out = result['timed_out']
    total = result['hits']['total']['value']
    logger.debug('{id},{total},{url},'.format(id=id,total=total,url=url))

    return is_time_out == False and total > 0
