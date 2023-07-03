# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CouncilItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    council_id = scrapy.Field()
    data = scrapy.Field()
    # metting_data = scrapy.Field()
    # vote_data = scrapy.Field()
    documents = scrapy.Field()
    activities = scrapy.Field()