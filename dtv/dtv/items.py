# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DtvItem(scrapy.Item):
    Likes = scrapy.Field()
    Playback_volume = scrapy.Field()
    Number_of_barrages = scrapy.Field()
    Number_of_coins_invested = scrapy.Field()
    Collection_volume = scrapy.Field()
    Forwarding_volume = scrapy.Field()
    title = scrapy.Field()
    # name = scrapy.Field()

