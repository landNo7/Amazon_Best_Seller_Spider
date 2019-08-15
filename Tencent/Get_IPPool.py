from lxml import etree
import requests
import time
import threading
import IPPool

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/\
    signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.xicidaili.com',
    'If-None-Match': 'W/"ffb4b53d0b5b26754318e4ece433fa9b"',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.38\
    09.100 Safari/537.36',
}


# 获取代理IP的线程类
class GetIpThread(threading.Thread):

    def __init__(self, url, sleep_time):
        super(GetIpThread, self).__init__()
        self.sleep_time = sleep_time
        self.url = url

    def run(self):
        while True:
            page = requests.session()
            page.headers = header
            p = page.get(self.url)
            html = etree.HTML(p.text)
            # print(p.status_code)
            # print((etree.tostring(html)).decode("utf-8"))
            ip_pools = html.xpath('//*[@id="ip_list"]/tr/td[2]/text()')
            ip_port = html.xpath('//*[@id="ip_list"]/tr/td[3]/text()')
            ip_type = html.xpath('//*[@id="ip_list"]/tr/td[6]/text()')
            for i in range(0, len(ip_pools)):
                if ip_type[i] == 'HTTPS':
                    ip = 'https://' + ip_pools[i] + ':' + ip_port[i]
                    print(ip)
                    self.inspect_ip(ip)
            time.sleep(self.sleep_time)

    def inspect_ip(self, ip_port):
        # time.sleep(1)
        _header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng\
            ,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.baidu.com',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
             like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        }
        try:
            url = 'https://www.amazon.com'
            proxies = {"https": ip_port}
            requests.packages.urllib3.disable_warnings()
            s = requests.session()
            s.keep_alive = False
            request = s.get(url, headers=_header, proxies=proxies)
            if request.status_code == 200:
                print('可用代理' + ip_port)
                IPPool.add_ip(ip_port)
            else:
                print('不可用代理' + ip_port)
        except requests.exceptions.ProxyError:
            pass


if __name__ == '__main__':
    G = GetIpThread('https://www.xicidaili.com/nn/', 5)
    G.start()
