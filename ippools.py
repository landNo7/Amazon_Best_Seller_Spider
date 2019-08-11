from lxml import etree
from bs4 import BeautifulSoup
from lxml import html
import requests
import urllib
import ast
import re
import os

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.xicidaili.com',
    'If-None-Match': 'W/"ffb4b53d0b5b26754318e4ece433fa9b"',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}

url = "https://www.xicidaili.com/nn/"

page = requests.session()
page.headers = header

p = page.get(url)

html = etree.HTML(p.text)
print(p.status_code)
# print((etree.tostring(html)).decode("utf-8"))
ip_pool = html.xpath('//*[@id="ip_list"]/tr/td[2]/text()')
ip_type = html.xpath('//*[@id="ip_list"]/tr/td[6]/text()')
# print(ip_pool)
# print(ip_type)
pools = []
for i in range(0, len(ip_pool)):
    if ip_type[i] == 'HTTPS':
        ip = 'https://' + ip_pool[i]
        pools.append(ip)
        print(ip)

