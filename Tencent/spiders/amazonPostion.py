# -*- coding: utf-8 -*-
import scrapy
import math
import os
import re

from Tencent.items import TencentItem, UrlItem
from scrapy_redis.spiders import RedisSpider

error_report = '.\\Data\\error_report'
file_dir = '.\\Data'
file_name = 'Home&Kitchen'
search_key = 'Home&Kitchen'

star_num_limit = 1000
star_limit = 4.3
DOWNLOAD_DELAY = 0.3
CONCURRENT_REQUESTS_PER_DOMAIN = 16

crawl_depth = 4
url_start_depth = 2
crawl_depth = crawl_depth - url_start_depth - 1
is_full_page = 1
url_list = [
    'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bar-Tools-Drinkware/zgbs/kitchen/289728/ref=zg_bs_nav_k_1_k',
    'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Wine-Accessories/zgbs/kitchen/13299291/ref=zg_bs_nav_k_1_k',
    'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Utensils-Gadgets/zgbs/kitchen/289754/ref=zg_bs_nav_k_1_k',
    'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Storage-Organization/zgbs/kitchen/510136/ref=zg_bs_nav_k_1_k',
    'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Entertaining/zgbs/kitchen/13162311/ref=zg_bs_nav_k_1_k'
]
title_ignore = []

failed_path = os.path.join(error_report, "failed.txt")
three_level_url_path = os.path.join(error_report, "Three_level_url.txt")
url_path = os.path.join(error_report, "url.txt")
base_url = 'https://www.amazon.com'
reviews_url = 'https://www.amazon.com/product-reviews/'
crawl_url = 'https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0'
next_page_url_end = '?_encoding=UTF8&pg=2'
# 大类小类列表xpath
xpath_plus = 'ul/'
xpath_start = '//*[@id="zg_browseRoot"]/ul/' + url_start_depth * xpath_plus
xpath_end = 'li/a/'
# 匹配非法字符
r_str = r"[\/\\\:\'\*\?\"\<\>\|\n\r]"
# 获取动态ip
get_ip_url = 'http://api.ip.data5u.com/dynamic/get.html?order=e6913d3978399fbebaf814a6cb554bf8&sep=3'
# 获取时间间隔
Thread_sleep_time = 5.5


class AmazonSpider(RedisSpider):
    name = 'amazonSpider'
    redis_key = "amazonspider:start_urls"
    # start_urls = [
    #     'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bar-Tools-Drinkware/zgbs/kitchen/289728/ref=zg_bs_nav_k_1_k',
    #     'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Wine-Accessories/zgbs/kitchen/13299291/ref=zg_bs_nav_k_1_k'
    # ]
    custom_settings = {
        "DOWNLOAD_DELAY": DOWNLOAD_DELAY,
        "CONCURRENT_REQUESTS_PER_DOMAIN": CONCURRENT_REQUESTS_PER_DOMAIN
    }

    def parse(self, response):
        response.meta['max_retry_times'] = 1
        if not os.path.exists(error_report):
            os.mkdir(error_report)
        items = []
        xpath = xpath_start + xpath_end
        parent_url_list = response.xpath(xpath + '@href').extract()
        parent_title_list = response.xpath(xpath + 'text()').extract()

        for i in range(0, len(parent_url_list)):
            item = self.meta_to_item(level_title=search_key + '/' + re.sub(r_str, "_", parent_title_list[i]),
                                     level_url=parent_url_list[i])
            items.append(item)
        # 进入下一级分类
        for item in items:
            yield scrapy.Request(url=item['level_url'],
                                 meta={'meta_1': item, 'current_depth': 1},
                                 callback=self.next_parse)

    def next_parse(self, response):
        # 提取出传过来的item
        meta_1 = response.meta['meta_1']
        current_depth = response.meta['current_depth']
        xpath = xpath_start + xpath_plus * current_depth + xpath_end
        level_url_list = response.xpath(xpath + '@href').extract()
        level_title_list = response.xpath(xpath + 'text()').extract()
        items = []
        # 当前分类无小分类
        if not level_url_list:
            # 前50产品
            items = self.max_depth(response, meta_1)
            for item in items:
                yield scrapy.Request(url=item['reviews_url'], meta={'meta_3': item}, callback=self.detail_parse)
            # 爬取第二页
            yield scrapy.Request(url=response.url + next_page_url_end,
                                 meta={'meta_2': meta_1},
                                 callback=self.rank_parse)
        # 当前分类已到爬取深度
        elif current_depth == crawl_depth:
            level_url_list = self.double_page(level_url_list)
            for i in range(0, len(level_url_list)):
                item = self.meta_to_item(level_title=meta_1['level_title'] + '/' + re.sub(r_str, "_",
                                                                                          level_title_list[int(i / 2)]),
                                         level_url=level_url_list[i])
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['level_url'], meta={'meta_2': item}, callback=self.rank_parse)
        # 当前分类未到指定深度
        else:
            for i in range(0, len(level_url_list)):
                item = self.meta_to_item(
                    level_title=meta_1['level_title'] + '/' + re.sub(r_str, "_", level_title_list[i]),
                    level_url=level_url_list[i])
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['level_url'],
                                     meta={'meta_1': item, 'current_depth': current_depth + 1},
                                     callback=self.next_parse)

    # 获取当前页面所有商品链接
    def rank_parse(self, response):
        # 提取item
        meta_2 = response.meta['meta_2']
        items = self.max_depth(response, meta_2)
        for item in items:
            yield scrapy.Request(url=item['reviews_url'], meta={'meta_3': item}, callback=self.detail_parse)

    # 进入product_reviews界面爬取价格、评分等数据
    def detail_parse(self, response):
        item = response.meta['meta_3']
        product_price = response.xpath('//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[4]/span\
        /span[3]/text()').extract()
        product_stars = response.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/a/span/text()').extract()
        reviews_num = response.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span\
        /text()').extract()
        product_5star = response.xpath('//*[@class="a-meter 5star"]/@aria-label').extract()
        product_4star = response.xpath('//*[@class="a-meter 4star"]/@aria-label').extract()

        try:
            item['product_stars'] = float(re.findall(r'\d+.\d+', product_stars[0])[0])
            # 超过一千时爬取的评价数中有','
            review_num = ''
            for num in reviews_num[0].split(','):
                review_num += num
            item['reviews_num'] = int(review_num)
            # 提前过滤评分低于要求个评论数量超过要求的产品
            if item['product_stars'] >= star_limit or item['reviews_num'] < star_num_limit:
                page_num = math.ceil(item['reviews_num'] / 10)
                rate = (int(re.findall(r'\d+', product_5star[0])[0]) + int(
                    re.findall(r'\d+', product_4star[0])[0])) / 100.0
                item['product_price'] = product_price[0]
                item['star_num'] = round(item['reviews_num'] * rate, 2)
                # 评论最后一页url
                url = item['reviews_url'] + '?sortBy=recent&pageNumber={num}'.format(num=page_num)
                yield scrapy.Request(url=url, meta={'meta_4': item}, callback=self.earliest_review_pasre)
            else:
                print('Exceed the limit', item['product_stars'], item['reviews_num'])
        except IndexError:
            # 被Amazon拒绝掉的请求
            with open(failed_path, 'a+') as err:
                err.write(str(item['product_asin']) + '\n')

    # 爬取评价页最后一页的最后一个评价的时间
    def earliest_review_pasre(self, response):
        item = response.meta['meta_4']
        earliest_date_list = response.xpath('//*[@class="a-section review aok-relative"]/div/div/span/text()').extract()
        if not earliest_date_list:
            item['earliest_date'] = 'crawl failed'
        else:
            item['earliest_date'] = earliest_date_list[len(earliest_date_list) - 1]
        if item['product_stars'] >= star_limit or item['reviews_num'] < star_num_limit:
            yield item

    def meta_to_item(self, level_title=None, level_url=None, product_name=None, product_url=None,
                     product_asin=None, product_image_url=None, _reviews_url=None):
        item = TencentItem()
        item['level_title'] = level_title
        item['level_url'] = level_url
        item['product_name'] = product_name
        item['product_url'] = product_url
        item['product_asin'] = product_asin
        item['product_image_url'] = product_image_url
        item['reviews_url'] = _reviews_url
        return item

    # 分类两页url
    def double_page(self, _url_list):
        temp = []
        for url in _url_list:
            temp.append(url)
            temp.append(url + next_page_url_end)
        return temp

    # 无小分类时直接爬取当前页产品存到items
    def max_depth(self, response, meta):
        items = []
        product_url_list = response.xpath('//*[@class="zg-item-immersion"]/span/div/span/a[@class="a-link-normal"]\
                                                                                                    /@href').extract()
        product_name_list = response.xpath('//*[@id="zg-ordered-list"]/li/span/div/span/a/span/div/img/@alt').extract()
        img_url_list = response.xpath('//*[@id="zg-ordered-list"]/li/span/div/span/a/span/div/img/@src').extract()

        for i in range(0, len(product_url_list)):
            name = re.sub(r_str, "_", product_name_list[i])
            try:
                url_chip = product_url_list[i].split('/')
                asin = ''
                for j in range(0, len(url_chip)):
                    if url_chip[j] == 'dp':
                        asin = url_chip[j + 1].split('?')[0]
                        break
                url = reviews_url + asin
                img_url = img_url_list[i]
                item = self.meta_to_item(level_title=meta['level_title'],
                                         level_url=response.url,
                                         product_name=name,
                                         product_url=base_url + product_url_list[i],
                                         product_asin=asin,
                                         product_image_url=img_url,
                                         _reviews_url=url)
                items.append(item)
            except IndexError:
                with open(url_path, 'a+') as err:
                    err.write(base_url + product_url_list[i])
        return items

# class AmazonUrlSpider(scrapy.Spider):
#     name = 'urlSpider'
#     redis_key = "amazonspider:start_urls"
#     start_urls = [
#         'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bar-Tools-Drinkware/zgbs/kitchen/289728/ref=zg_bs_nav_k_1_k',
#         'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Wine-Accessories/zgbs/kitchen/13299291/ref=zg_bs_nav_k_1_k'
#     ]
#     custom_settings = {
#         "DOWNLOAD_DELAY": DOWNLOAD_DELAY,
#         "CONCURRENT_REQUESTS_PER_DOMAIN": CONCURRENT_REQUESTS_PER_DOMAIN
#     }
#
#     def parse(self, response):
#         response.meta['max_retry_times'] = 1
#         xpath = xpath_start + xpath_end
#         parent_url_list = response.xpath(xpath+'@href').extract()
#         for i in range(0, len(parent_url_list)):
#             yield scrapy.Request(url=parent_url_list[i],
#                                  meta={'current_depth': 1},
#                                  callback=self.next_parse)
#
#     def next_parse(self, response):
#         current_depth = response.meta['current_depth']
#         xpath = xpath_start + xpath_plus * current_depth + xpath_end
#         level_url_list = response.xpath(xpath+'@href').extract()
#         if not level_url_list:
#             item = UrlItem()
#             item['url'] = response.url
#             yield item
#             item1 = UrlItem()
#             item1['url'] = response.url+next_page_url_end
#             yield item1
#         elif current_depth == crawl_depth:
#             for url in self.double_page(level_url_list):
#                 item = UrlItem()
#                 item['url'] = url
#                 yield item
#         else:
#             for i in range(0, len(level_url_list)):
#                 yield scrapy.Request(url=level_url_list[i],
#                                      meta={'current_depth': current_depth + 1},
#                                      callback=self.next_parse)
#
#     # 分类两页url
#     def double_page(self, _url_list):
#         temp = []
#         for url in _url_list:
#             temp.append(url)
#             temp.append(url + next_page_url_end)
#         return temp
