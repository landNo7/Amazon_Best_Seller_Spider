# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlItem(scrapy.Item):
    url = scrapy.Field()


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    level_title = scrapy.Field()
    level_url = scrapy.Field()
    product_name = scrapy.Field()
    product_url = scrapy.Field()
    product_asin = scrapy.Field()
    product_image_url = scrapy.Field()
    reviews_url = scrapy.Field()

    product_price = scrapy.Field()
    product_stars = scrapy.Field()
    reviews_num = scrapy.Field()
    star_num = scrapy.Field()

    earliest_date = scrapy.Field()

    star_num_min_limit = scrapy.Field()
    star_num_max_limit = scrapy.Field()
    star_min_limit = scrapy.Field()
    star_max_limit = scrapy.Field()
    price_min_limit = scrapy.Field()
    price_max_limit = scrapy.Field()

