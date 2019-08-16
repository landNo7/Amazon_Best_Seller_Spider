import requests
import IPPool
import json


def meta_to_item(primary_title=None, primary_url=None, secondary_title=None, secondary_url=None,
                 three_level_title=None, three_level_url=None, four_level_title=None, four_level_url=None,
                 reviews_url=None, product_url=None, product_name=None, product_asin=None, product_image_url=None,
                 file_dir=None):
    item = {'primary_title': primary_title, 'primary_url': primary_url, 'secondary_title': secondary_title,
            'secondary_url': secondary_url, 'three_level_title': three_level_title, 'three_level_url': three_level_url,
            'four_level_title': four_level_title, 'four_level_url': four_level_url, 'reviews_url': reviews_url,
            'product_url': product_url, 'product_name': product_name, 'product_asin': product_asin,
            'product_image_url': product_image_url, 'file_dir': file_dir}
    print(item)


_header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng\
            ,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
             like Gecko) Chrome/76.0.3809.100 Safari/537.36',
}
# print(meta_to_item(primary_title='ddd', primary_url='dss'))
try:

    url = 'https://www.amazon.com'
    ip_port = IPPool.app_ip()
    proxies = {"https": ip_port}
    print(ip_port)
    requests.packages.urllib3.disable_warnings()
    s = requests.session()
    s.keep_alive = False
    request = s.get(url, headers=_header, proxies=proxies)
    print(request.status_code)
    # print(request.text)
    if request.status_code == 200:
        print('可用代理' + ip_port)
    else:
        print('不可用代理' + ip_port)
except requests.exceptions.ProxyError:
    print('不可用代理1' + ip_port)

# List = [0, 1, 2, 3, 4]
# for i in range(0, len(List)):
#     List.append(i+5)
#     print(i)
