from ..settings import *

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['crawl2020-demo.com']
ELASTICSEARCH_CONNECTIONS['default']['URL'] = 'http://crawl2020_elasticsearch:9200/'
