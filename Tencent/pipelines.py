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
from Tencent.spiders.amazonPostion import file_dir, search_key, star_num_limit, star_limit
from Tencent.spiders.amazonPostion import error_report as er
from Tencent.middlewares import thread_g


class TencentPipeline(object):

    error_report = er

    def __init__(self):
        self.star_num_limit = star_num_limit
        self.star_limit = star_limit
    # 创建一个excel文件
    #     self.workbook = xlsxwriter.Workbook(os.path.join(file_dir, '{name}.xlsx'.format(name=search_key)))
    # 在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
    #     self.worksheet = self.workbook.add_worksheet(u'sheet1')
    #     title_list = ['title', 'url', 'price', 'stars', 'reviews_num', 'star_num', 'earliest_date']
    #     self.worksheet.write_row(0, 0, title_list)
    #     self.worksheet.set_column(0, 0, 100)
    #     self.worksheet.set_column(1, 1, 40)
    #     self.worksheet.set_column(2, 5, 10)
    #     self.worksheet.set_column(6, 6, 20)
    #     self.row = 1

    def process_item(self, item, spider):
        if item['star_num'] or item['star_num'] == 0.0:
            if item['star_num'] < self.star_num_limit and item['product_stars'] >= self.star_limit:
                data = [item['product_name'], item['product_url'], item['product_price'], item['product_stars'],
                        item['reviews_num'], item['star_num'], item['earliest_date'], item['level_title']]
                self.worksheet.write_row(self.row, 0, data)
                self.row += 1
                print(item['product_name']+'saved!')
            else:
                path = os.path.join(self.error_report, 'Exceed.txt')
                with open(path, 'a+') as err:
                    err.write(str(item['product_asin']) + ' ' + str(item['star_num']) + ' ' + str(
                        item['product_stars']) + '\n')
                raise DropItem('Exceed the limit ', item['product_stars'], item['star_num'])
        else:
            path = os.path.join(self.error_report, 'Not_stars.txt')
            with open(path, 'a+') as err:
                err.write(str(item['product_asin']) + '\n')
            raise DropItem('Not_stars at %s' % item['product_asin'])
        # self.worksheet.write(self.row, 0, item['url'])
        # self.row += 1
        # return item

    def close_spider(self, spider):
        #self.workbook.close()
        if thread_g.isAlive():
            thread_g.close()
            thread_g.join()

