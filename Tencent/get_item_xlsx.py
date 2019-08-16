import IPPool
import xlsxwriter
import os

file_dir = '.\\'
file_name = 'test'
num_limit = 1000
star_limit = 4.3
# 创建一个excel文件
workbook = xlsxwriter.Workbook(os.path.join(file_dir, '{name}.xlsx'.format(name=file_name)))
# 在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
worksheet = workbook.add_worksheet(u'sheet1')
title_list = ['title', 'url', 'price', 'stars', 'reviews_num', 'star_num', 'earliest_date']
worksheet.write_row(0, 0, title_list)
worksheet.set_column(0, 0, 100)
worksheet.set_column(1, 1, 40)
worksheet.set_column(2, 5, 10)
worksheet.set_column(6, 6, 20)
row = 1


item = IPPool.get_item()
while item:
    if item['reviews_num'] > num_limit or item['product_stars'] < star_limit:
        print(item)
    else:
        data = [item['product_name'], item['product_url'], item['product_price'], item['product_stars'],
                item['reviews_num'], item['star_num'], item['earliest_date'], item['level_title']]
        worksheet.write_row(row, 0, data)
        row += 1
    item = IPPool.get_item()

workbook.close()
