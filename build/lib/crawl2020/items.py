# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    crawlOn = scrapy.Field()
    postOn = scrapy.Field()
    postBy = scrapy.Field()
    source = scrapy.Field()
    spider = scrapy.Field()
    taskName = scrapy.Field()
    text = scrapy.Field()
    html = scrapy.Field()
    spiderTags = scrapy.Field()
    tags = scrapy.Field()

    def __str__(self) -> str:
        return '{0}\t{1}'.format(self['title'], self['url'])