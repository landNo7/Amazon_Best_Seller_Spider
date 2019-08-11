# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    primary_title = scrapy.Field()
    primary_url = scrapy.Field()

    secondary_title = scrapy.Field()
    secondary_url = scrapy.Field()

    three_level_title = scrapy.Field()
    three_level_url = scrapy.Field()

    four_level_title = scrapy.Field()
    four_level_url = scrapy.Field()

    file_dir = scrapy.Field()

    product_name = scrapy.Field()
    product_url = scrapy.Field()

    product_asin = scrapy.Field()
    product_image_url = scrapy.Field()
    product_price = scrapy.Field()
    product_stars = scrapy.Field()
    reviews_num = scrapy.Field()
    star_num = scrapy.Field()
    # earliest_date = scrapy.Field()


