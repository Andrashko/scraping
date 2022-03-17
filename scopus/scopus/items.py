# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScopusItem(scrapy.Item):
    name = scrapy.Field()
    keywords = scrapy.Field()
    publications  = scrapy.Field()
    documents  = scrapy.Field()
    citations = scrapy.Field()
    h = scrapy.Field()