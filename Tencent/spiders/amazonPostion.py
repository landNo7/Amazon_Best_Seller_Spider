# -*- coding: utf-8 -*-
import scrapy
import os
import re
import sys
from scrapy.exceptions import DropItem
from Tencent.items import TencentItem
from Tencent.Get_IPPool import GetIpThread
import math

error_report = '.\\Data\\error_report'
file_dir = '.\\Data'
search_key = 'Home&Kitchen'
# search_key = 'Kitchen & Dining'
crawl_url = 'https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0'
star_num_limit = 1000
star_limit = 4.3
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 16
failed_path = os.path.join(error_report, "failed.txt")
three_level_url_path = os.path.join(error_report, "Three_level_url.txt")
url_path = os.path.join(error_report, "url.txt")


class AmazonSpider(scrapy.Spider):
    name = 'amazonSpider'
    allowed_domains = ['www.amazon.com']
    base_url = 'https://www.amazon.com'
    start_urls = [crawl_url]
    reviews_url = 'https://www.amazon.com/product-reviews/'
    r_str = r"[\/\\\:\'\*\?\"\<\>\|\n\r]"
    custom_settings = {
        "DOWNLOAD_DELAY": DOWNLOAD_DELAY,
        "CONCURRENT_REQUESTS_PER_DOMAIN": CONCURRENT_REQUESTS_PER_DOMAIN
    }

    def parse(self, response):
        response.meta['max_retry_times'] = 3
        items_dir = os.path.join(file_dir, search_key)
        if not os.path.exists(items_dir):
            os.makedirs(items_dir)
        if not os.path.exists(error_report):
            os.mkdir(error_report)
        items = []
        # 二级分类链接列表
        secondary_url_list = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/li/a/@href').extract()
        # 二级分类名称列表
        secondary_classname_list = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/li/a/text()').extract()

        for i in range(0, len(secondary_url_list)):
            name = secondary_classname_list[i]
            name = re.sub(self.r_str, "_", name)
            url = secondary_url_list[i]
            secondary_dir = os.path.join(items_dir, name)
            if not os.path.exists(secondary_dir):
                os.mkdir(secondary_dir)
            # 生成每个二级分类的item
            item = TencentItem()
            item['primary_title'] = search_key
            item['primary_url'] = self.start_urls[0]
            item['secondary_title'] = name
            item['secondary_url'] = url
            item['file_dir'] = secondary_dir
            items.append(item)
        # 递归进入三级分类
        for item in items:
            yield scrapy.Request(url=item['secondary_url'], meta={'meta_1': item}, callback=self.second_parse)

    def second_parse(self, response):
        # 提取出传过来的item
        meta_1 = response.meta['meta_1']

        # 三级分类链接列表
        three_level_url_list = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/@href').extract()
        # 三级分类名称列表
        three_level_classname_list = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/li/a/text()').extract()
        # 创建三级分类字典

        items = []

        for i in range(0, len(three_level_url_list)):
            name = three_level_classname_list[i]
            name = re.sub(self.r_str, "_", name)
            url = three_level_url_list[i]
            three_level_dir = os.path.join(meta_1['file_dir'], name)
            if not os.path.exists(three_level_dir):
                os.mkdir(three_level_dir)
            item = TencentItem()
            item['primary_title'] = meta_1['primary_title']
            item['primary_url'] = meta_1['primary_url']
            item['secondary_title'] = meta_1['secondary_title']
            item['secondary_url'] = meta_1['secondary_url']
            item['three_level_title'] = name
            item['three_level_url'] = url
            item['file_dir'] = three_level_dir
            items.append(item)
        for item in items:
            yield scrapy.Request(url=item['three_level_url'], meta={'meta_2': item}, callback=self.third_parse)

    def third_parse(self, response):
        # 提取出传过来的item
        meta_2 = response.meta['meta_2']
        # 四级分类链接列表
        four_level_url_list = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/@href').extract()
        # 四级分类名称列表
        four_level_classname_list = response.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/text()').extract()
        # 创建四级分类字典
        if not four_level_url_list:
            meta_2['four_level_title'] = 'no four level'
            meta_2['four_level_url'] = 'no four level'
            with open(three_level_url_path, 'a+') as err:
                err.write(str(meta_2['three_level_url']) + '\n')
            yield scrapy.Request(url=meta_2['three_level_url'], meta={'meta_3': meta_2}, callback=self.rank_parse)
        else:
            items = []

            for i in range(0, len(four_level_url_list)):
                name = four_level_classname_list[i]
                name = re.sub(self.r_str, "_", name)
                url = four_level_url_list[i]
                four_level_dir = os.path.join(meta_2['file_dir'], name)
                if not os.path.exists(four_level_dir):
                    os.mkdir(four_level_dir)
                item = TencentItem()
                item['primary_title'] = meta_2['primary_title']
                item['primary_url'] = meta_2['primary_url']
                item['secondary_title'] = meta_2['secondary_title']
                item['secondary_url'] = meta_2['secondary_url']
                item['three_level_title'] = meta_2['three_level_title']
                item['three_level_url'] = meta_2['three_level_url']
                item['four_level_title'] = name
                item['four_level_url'] = url
                item['file_dir'] = four_level_dir
                items.append(item)
            for item in items:
                yield scrapy.Request(url=item['four_level_url'], meta={'meta_3': item}, callback=self.rank_parse)

    # 获取当前页面所有商品链接
    def rank_parse(self, response):
        # 提取item
        meta_3 = response.meta['meta_3']
        items = []
        # 商品链接列表
        product_url_list = response.xpath('//*[@class="zg-item-immersion"]/span/div/span/a[@class="a-link-normal"]\
        /@href').extract()
        product_name_list = response.xpath('//*[@id="zg-ordered-list"]/li/span/div/span/a/span/div/img/@alt').extract()
        img_url_list = response.xpath('//*[@id="zg-ordered-list"]/li/span/div/span/a/span/div/img/@src').extract()

        for i in range(0, len(product_url_list)):
            name = product_name_list[i]
            # 商品文件夹路径
            name = re.sub(self.r_str, "_", name)
            try:
                url_chip = product_url_list[i].split('/')
                asin = ''
                for j in range(0, len(url_chip)):
                    if url_chip[j] == 'dp':
                        asin = url_chip[j+1].split('?')[0]
                        break
                url = self.reviews_url + asin
                product_dir = os.path.join(meta_3['file_dir'], asin)
                img_url = img_url_list[i]
                item = TencentItem()
                item['primary_title'] = meta_3['primary_title']
                item['primary_url'] = meta_3['primary_url']
                item['secondary_title'] = meta_3['secondary_title']
                item['secondary_url'] = meta_3['secondary_url']
                item['three_level_title'] = meta_3['three_level_title']
                item['three_level_url'] = meta_3['three_level_url']
                item['four_level_title'] = meta_3['four_level_title']
                item['four_level_url'] = meta_3['four_level_url']
                item['reviews_url'] = url
                item['product_url'] = self.base_url + product_url_list[i]
                item['product_name'] = name
                item['product_asin'] = asin
                item['product_image_url'] = img_url
                item['file_dir'] = product_dir
                items.append(item)
            except IndexError:
                with open(url_path, 'a+') as err:
                    err.write(str(product_url_list[i]))
        for item in items:
            yield scrapy.Request(url=item['reviews_url'], meta={'meta_4': item}, callback=self.detail_parse)

    # 进入product_reviews界面爬取价格、评分等数据
    def detail_parse(self, response):
        item = response.meta['meta_4']
        product_price = response.xpath('//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[4]/span\
        /span[3]/text()').extract()
        product_stars = response.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/a/span/text()').extract()
        reviews_num = response.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span\
        /text()').extract()
        product_5star = response.xpath('//*[@class="a-meter 5star"]/@aria-label').extract()
        product_4star = response.xpath('//*[@class="a-meter 4star"]/@aria-label').extract()

        try:
            item['product_stars'] = float(re.findall(r'\d+.\d+', product_stars[0])[0])
            # item['reviews_num'] = int(re.findall(r'\d+', reviews_num[0])[0])
            review_num = ''
            for num in reviews_num[0].split(','):       # 超过一千时爬取的评价数中有','
                review_num += num
            item['reviews_num'] = int(review_num)
            if item['product_stars'] < star_limit or item['reviews_num'] > star_num_limit:  # 提前过滤评分低于要求个评论数量超过要求的产品
                pass
            page_num = math.ceil(item['reviews_num']/10)
            rate = (int(re.findall(r'\d+', product_5star[0])[0]) + int(re.findall(r'\d+', product_4star[0])[0])) / 100.0
            item['product_price'] = product_price[0]
            item['star_num'] = round(item['reviews_num'] * rate, 2)
            url = item['reviews_url'] + '?sortBy=recent&pageNumber={num}'.format(num=page_num)  # 评论最后一页url
            yield scrapy.Request(url=url, meta={'meta_5': item}, callback=self.earliest_review_pasre)
        except IndexError:  # 被Amazon拒绝掉的请求
            with open(failed_path, 'a+') as err:
                err.write(str(item['product_asin'])+' '+str(item['file_dir'])+'\n')

    # 爬取评价页最后一页的最后一个评价的时间
    def earliest_review_pasre(self, response):
        item = response.meta['meta_5']
        earliest_date_list = response.xpath('//*[@class="a-section review aok-relative"]/div/div/span/text()').extract()
        if not earliest_date_list:
            url = item['reviews_url'] + '?sortBy=recent&pageNumber={num}'.format(
                num=math.ceil(item['reviews_num']/10)-1)        # 评论最后一页url
            yield scrapy.Request(url=url, meta={'meta_5': item}, callback=self.earliest_review_pasre)
        else:
            item['earliest_date'] = earliest_date_list[len(earliest_date_list) - 1]
            yield item
