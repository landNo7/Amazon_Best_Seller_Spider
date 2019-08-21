# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from scrapy_redis import connection, defaults
from twisted.internet.threads import deferToThread

default_serialize = ScrapyJSONEncoder().encode


class RedisPipeline(object):
    """Pushes serialized item into a redis list/queue

    Settings
    --------
    REDIS_ITEMS_KEY : str
        Redis key where to store items.
    REDIS_ITEMS_SERIALIZER : str
        Object path to serializer function.

    """

    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        """Initialize pipeline.

        Parameters
        ----------
        server : StrictRedis
            Redis client instance.
        key : str
            Redis key where to store items.
        serialize_func : callable
            Items serializer function.

        """
        self.server = server
        self.key = key
        self.serialize = serialize_func

    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )

        return cls(**params)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        if item['star_num'] or item['star_num'] == 0.0:
            if item['star_num_max_limit'] >= item['star_num'] >= item['star_num_min_limit'] and \
                    item['star_max_limit'] >= item['product_stars'] >= item['star_min_limit']:
                price = float(re.findall(r'\d+.\d+', item['product_price'])[0])
                if item['price_max_limit'] >= price >= item['price_min_limit']:
                    return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.serialize(item)
        self.server.rpush(key, data)
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider.

        Override this function to use a different key depending on the item
        and/or spider.

        """
        return self.key % {'spider': spider.name}


# class TencentPipeline(object):
#     error_report = er
#
#     def __init__(self):
#         self.star_num_limit = star_num_limit
#         self.star_limit = star_limit
#
#         # 创建一个excel文件
#         self.workbook = xlsxwriter.Workbook(os.path.join(file_dir, '{name}.xlsx'.format(name='crawl')))
#         # 在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
#         self.worksheet = self.workbook.add_worksheet(u'sheet1')
#         title_list = ['title', 'url', 'price', 'stars', 'reviews_num', 'star_num', 'earliest_date']
#         self.worksheet.write_row(0, 0, title_list)
#         self.worksheet.set_column(0, 0, 100)
#         self.worksheet.set_column(1, 1, 40)
#         self.worksheet.set_column(2, 5, 10)
#         self.worksheet.set_column(6, 6, 20)
#         self.row = 1
#
#     def process_item(self, item, spider):
#         if item['star_num'] or item['star_num'] == 0.0:
#             if item['star_num'] < self.star_num_limit and item['product_stars'] >= self.star_limit:
#                 data = [item['product_name'], item['product_url'], item['product_price'], item['product_stars'],
#                         item['reviews_num'], item['star_num'], item['earliest_date'], item['level_title']]
#                 self.worksheet.write_row(self.row, 0, data)
#                 self.row += 1
#                 print(item['product_name'] + 'saved!')
#             else:
#                 path = os.path.join(self.error_report, 'Exceed.txt')
#                 with open(path, 'a+') as err:
#                     err.write(str(item['product_asin']) + ' ' + str(item['star_num']) + ' ' + str(
#                         item['product_stars']) + '\n')
#                 raise DropItem('Exceed the limit ', item['product_stars'], item['star_num'])
#         else:
#             path = os.path.join(self.error_report, 'Not_stars.txt')
#             with open(path, 'a+') as err:
#                 err.write(str(item['product_asin']) + '\n')
#             raise DropItem('Not_stars at %s' % item['product_asin'])
#
#     def close_spider(self, spider):
#         self.workbook.close()

