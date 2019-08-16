from lxml import etree
from bs4 import BeautifulSoup
from lxml import html
import requests
import urllib
import ast
import re
import os
import math
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.amazon.com/gp/bestsellers',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

header1 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;\
    q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Baking\
    -Supplies/zgbs/home-garden/2231407011/ref=zg_bs_nav_hg_2_3206325011',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

header2 = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/\
    webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'Host': 'www.amazon.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

image_header = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53\
    7.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}

baking_header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/\
    webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Store/\
    zgbs/home-garden/3206325011/ref=zg_bs_unv_hg_2_2231407011_1',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.\
    36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}
amazon_url = 'https://www.amazon.com/dp/B07VYWRKJD/ref=twister_B07VSYP6V4?_encoding=UTF8&psc=1'

stars_url = 'https://www.amazon.com/gp/customer-reviews/widgets/average-custo\
mer-review/popover/ref=dpx_acr_pop_?asin=B0751JFFYY'
params = {
    'contextId': 'dpx',
    'asin': 'B0751JFFYY'
}
three_level_url = 'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bar-Tools-Drinkware\
/zgbs/kitchen/289728/ref=zg_bs_nav_k_1_k'

baking_url = 'https://www.amazon.com/Best-Sellers-Home-Kitchen-Kids-Baking-Supp\
lies/zgbs/home-garden/2231407011/ref=zg_bs_nav_hg_2_3206325011'
url = 'https://www.amazon.com/product-reviews/B07GYR8NGX/?sortBy=recent&pageNumber=96'
search_url = 'https://www.amazon.com/s?k=iphone+x+case&lo=grid&page=2&qid=1565603710&ref=sr_pg_1'
page = requests.session()
page.headers = header
# print(math.ceil(90/10))
# p = page.get(amazon_url)
p = page.get(url=three_level_url)
print(p.status_code)
# print(p.url)
html = etree.HTML(p.text)
url_start_depth = 2
xpath_plus = 'ul/'
xpath_start = '//*[@id="zg_browseRoot"]/ul/' + url_start_depth * xpath_plus
xpath_end = 'li/a/'
parent_name = html.xpath('//*[@id="zg_browseRoot"]/ul/'+(url_start_depth-1) * xpath_plus + '\
        li/span/text()')
if parent_name:
    parent_name = parent_name[0]
else:
    parent_name = 'no name'
print(parent_name)

# next_page = html.xpath('//*[@class="a-last"]/a/@href')
# print(next_page)

# earliest_date = html.xpath('//*[@id="cm_cr-review_list"]/div[last()]/div/div/span/text()')
# earliest_date = html.xpath('//*[@class="a-section review aok-relative"]/div/div/span/text()')
# print(earliest_date[len(earliest_date) - 1])
# asin = html.xpath('//*[@data-component-type="sp-sponsored-result"]/../../../*[contains(@class,"AdHolder")]\
# /@data-asin')
# asin = html.xpath('//*[@data-component-type="sp-sponsored-result"]/../../../*[@class="sg-col\
# -4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 AdHolder\
# sg-col sg-col-4-of-20 sg-col-4-of-32"]/@data-asin')
# asin1 = html.xpath('//*[@data-component-type="sp-sponsored-result"]/../../@data-asin')
# asin += asin1
#
# print(len(asin))
# for ai in asin:
#     print(ai)
# //*[@id="a-autoid-13-announce"]
# color_list = html.xpath('//*[@id="variation_color_name"]/ul/li/span/div/span/span/span/button')
# print(color_list)
Sponsored_link = html.xpath('//*[contains(@class,"AdHolder")]/@data-asin')
print(len(Sponsored_link))
# for str in Sponsored_link:
#     print(str)
# reviews_num = html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span\
#         /text()')
# reviews_num = ['13,122,111']
# print(len(Sponsored))

# review_num = ''
# for num in reviews_num[0].split(','):
#     review_num += num
# if int(review_num) > 1000:
#     print(int(review_num))
# print(html.xpath('//*[@class="a-meter 5star"]/@aria-label'))
# print(html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/a/span/text()'))
# class_url = html.xpath('//*[@id="zg_browseRoot"]/ul/ul/ul/ul/li/a/@href')
# for i in range(0, len(class_url)):
#     print(1)
# for url in class_url:
#     print(url)
#
# product_url = html.xpath('//*[@id="zg-ordered-list"]/li/span/div/span/a/span/div/img/@src')
# print(len(product_url))
# n = 1
# for url in product_url:
#     print(str(n)+':'+url)
#     n += 1
# print((etree.tostring(html)).decode("utf-8"))
# product_name_list = html.xpath('//*[@id="zg-ordered-list"]/li/span/div/span/a/div/text()')
# product_class_list = html.xpath('//*[@id="zg_browseRoot"]/ul/ul/li/a/@href')
# product_asin = html.xpath('//*[@id="cerberus-data-metrics"]/@data-asin')
# product_stars = html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[3]/span/a/span/text()')
# product_5star = html.xpath('//*[@class="a-meter 5star"]/@aria-label')
# product_4star = html.xpath('//*[@class="a-meter 4star"]/@aria-label')
# product_price = html.xpath('//*[@id="cm_cr-product_info"]/div/div[2]/div/div/div[2]/div[4]/span/span[3]/text()')
# print(product_price)
# reviews_num = html.xpath('//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span/text()')
# num = int(re.findall(r'\d+', reviews_num[0])[0])
# print(num)
# for url in product_4star:
#     dicts = ast.literal_eval(url)
#     print(dicts['url'])
# for product in product_name_list
#     print(product)

# for product_type in product_class_list:
#     print(product_type)
# print(product_stars)
# print(product_asin)
# rate = (int(re.findall(r'\d+', product_5star[0])[0]) + int(re.findall(r'\d+', product_4star[0])[0])) / 100.0
# print(round(rate * num, 2))
# print(product_4star)
# image_url_list = html.xpath('//*[@id="zg-ordered-list"]/li/span/div/span/a/span/div/img/@src')
# n = 1
# for url in image_url_list:
#
#     print(url)
#     try:
#         pic = requests.get(url, timeout=10)
#         path = '.\\photo'
#         if not os.path.exists(path):
#             os.mkdir(path)
#         path = os.path.join(path, "{n}.jpg".format(n=str(n)))
#         with open(path, 'wb') as img:
#             img.write(pic.content)
#         print('download at ' + path)
#         n += 1
#     except:
#         print('download failed!')

# print(product_price)
# print(product_stars)
# print(re.findall(r'\d+.\d+', product_stars[0])[0])


# for stars in product_stars:
#     print("stars:", stars)
#
# for stars5 in product_5star:
#     print("5stars:", stars5)
#
# for stars4 in product_4star:
#     print("4stars:", stars4)

