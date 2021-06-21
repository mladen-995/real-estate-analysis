# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateItem(scrapy.Item):
    url = scrapy.Field()
    type = scrapy.Field()
    offer_type = scrapy.Field()
    city = scrapy.Field()
    city_part = scrapy.Field()
    address = scrapy.Field()
    area = scrapy.Field()
    price = scrapy.Field()
    build_year = scrapy.Field()
    area_field = scrapy.Field()
    level = scrapy.Field()
    total_level = scrapy.Field()
    registered = scrapy.Field()
    heating_type = scrapy.Field()
    number_of_rooms = scrapy.Field()
    number_of_toilets = scrapy.Field()
    has_elevator = scrapy.Field()
    has_balcony = scrapy.Field()
    has_parking = scrapy.Field()
    