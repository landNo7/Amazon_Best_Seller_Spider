import IPPool
import xlsxwriter
import os

file_dir = '.\\'


class get_excel(object):
    def __init__(self, file_name):
        key_name = file_name + ":items"
        # 创建一个excel文件
        workbook = xlsxwriter.Workbook(os.path.join(file_dir, '{name}.xlsx'.format(name=file_name)))
        # 在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
        worksheet = workbook.add_worksheet(u'sheet1')
        title_list = ['分类', '名称', '商品链接', '价格', '评分', '评价数量', '好评数量', '最后留评时间']
        worksheet.write_row(0, 0, title_list)
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 80)
        worksheet.set_column(2, 2, 40)
        worksheet.set_column(3, 6, 10)
        worksheet.set_column(7, 7, 20)
        row = 1
        try:
            item = IPPool.get_item1(key_name)
            while item:
                data = [item['level_title'], item['product_name'], item['product_url'], item['product_price'],
                        item['product_stars'], item['reviews_num'], item['star_num'], item['earliest_date']]
                worksheet.write_row(row, 0, data)
                row += 1
                item = IPPool.get_item1(key_name)
        except:
            pass
        workbook.close()
        print("打印完成")

