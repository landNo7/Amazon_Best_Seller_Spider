# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import os
import requests
from scrapy.exceptions import DropItem
import xlsxwriter
from Tencent.spiders.amazonPostion import search_key
from Tencent.spiders.amazonPostion import file_dir
from Tencent.spiders.amazonPostion import error_report as er


class TencentPipeline(object):
    max_price = 1000
    min_price = 10
    star_num_limit = 1000
    star_limit = 4.3
    error_report = er

    def __init__(self):
        self.workbook = xlsxwriter.Workbook(os.path.join(file_dir, '{name}.xlsx'.format(name=search_key)))  # 创建一个excel文件
        self.worksheet = self.workbook.add_worksheet(u'sheet1')  # 在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
        title_list = ['title', 'url', 'price', 'stars', 'reviews_num', 'star_num', 'earliest_date']
        self.worksheet.write_row(0, 0, title_list)
        self.worksheet.set_column(0, 0, 100)
        self.worksheet.set_column(1, 1, 40)
        self.worksheet.set_column(2, 5, 10)
        self.worksheet.set_column(6, 6, 20)
        self.row = 1

    def process_item(self, item, spider):
        if item['star_num'] or item['star_num'] == 0.0:
            if item['star_num'] < self.star_num_limit and item['product_stars'] >= self.star_limit:
                data = [item['product_name'], item['product_url'], item['product_price'], item['product_stars'],
                        item['reviews_num'], item['star_num'], item['earliest_date'], item['file_dir']]
                self.worksheet.write_row(self.row, 0, data)
                self.row += 1
                print(item['product_name']+'saved!')
            else:
                path = os.path.join(self.error_report, 'Exceed.txt')
                with open(path, 'a+') as err:
                    err.write(str(item['product_asin']) + ' ' + str(item['star_num']) + ' ' + str(
                        item['product_stars']) + '\n')
                raise DropItem('Exceed the limit %s' % item['product_asin'])
        else:
            path = os.path.join(self.error_report, 'Not_stars.txt')
            with open(path, 'a+') as err:
                err.write(str(item['product_asin']) + '\n')
            raise DropItem('Not_stars at %s' % item['product_asin'])

    def close_spider(self, spider):
        self.workbook.close()
    # def process_item(self, item, spider):
    #     if item['star_num'] or item['star_num'] == 0.0:
    #         if item['star_num'] < self.star_num_limit and item['product_stars'] >= self.star_limit:
    #             # try:
    #             if not os.path.exists(item['file_dir']):
    #                 os.mkdir(item['file_dir'])
    #             else:
    #                 raise DropItem('already download! %s' % item['product_asin'])
    #             pic = requests.get(item['product_image_url'], timeout=10)
    #             path = os.path.join(item['file_dir'], 'img.jpg')
    #             with open(path, 'wb') as img:
    #                 img.write(pic.content)
    #             print('download at ' + path)
    #             item_txt = os.path.join(item['file_dir'], 'detail.txt')
    #             with open(item_txt, 'w') as rt:
    #                 rt.write('name: ' + str(item['product_name']) + '\n' +
    #                          'url: ' + str(item['product_url']) + '\n' +
    #                          'asin: ' + str(item['product_asin']) + '\n' +
    #                          'price: ' + str(item['product_price']) + '\n' +
    #                          'stars: ' + str(item['product_stars']) + '\n' +
    #                          'reviews_num: ' + str(item['reviews_num']) + '\n' +
    #                          'star_num: ' + str(item['star_num']) + '\n')
    #             print(item['product_asin']+' '+str(item['product_stars'])+' '+str(item['star_num'])+' saved!')
    #             return item
    #             # except IOError:
    #             #     path = os.path.join(self.error_report, 'IOError.txt')
    #             #     with open(path, 'a+') as err:
    #             #         err.write(str(item['product_asin']) + ' ' + item['product_name'] + '\n')
    #             #     raise DropItem('IOError at %s' % item['product_asin'])
    #         else:
    #             path = os.path.join(self.error_report, 'Exceed.txt')
    #             with open(path, 'a+') as err:
    #                 err.write(str(item['product_asin']) + ' ' + str(item['star_num']) + ' ' + str(item['pro\
    #                 duct_stars']) + '\n')
    #             raise DropItem('Exceed the limit %s' % item['product_asin'])
    #     else:
    #         path = os.path.join(self.error_report, 'Not_stars.txt')
    #         with open(path, 'a+') as err:
    #             err.write(str(item['product_asin']) + '\n')
    #         raise DropItem('Not_stars at %s' % item['product_asin'])
    #
    # def stars_limit(self, item):
    #     if item['star_num'] < self.star_num_limit and item['product_stars'] >= self.star_limit:
    #         print('item num is {num},item star is {star}'.format(num=str(item['star_num']), star=str(item['p\
    #         roduct_stars'])))
    #         return 1
    #     return 0
    #
    # def price_limit(self, item):
    #     return 1
