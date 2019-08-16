from lxml import etree
import requests
import time
import threading
import Tencent.IPPool as IPPool

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/\
    signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
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
        self.flag = False

    def run(self):
        while True:
            if self.flag:
                break
            page = requests.session()
            page.headers = header
            p = page.get(self.url)
            # print(p.content)
            ip_port = "https://" + str(p.text.split('\n')[0])
            if IPPool.len_ip() < 30:
                IPPool.add_ip(ip_port)
            else:
                time.sleep(30)
                IPPool.rem_ip()
                IPPool.add_ip(ip_port)
            # _header = {
            #             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng\
            #                     ,*/*;q=0.8,application/signed-exchange;v=b3',
            #             'Accept-Encoding': 'gzip, deflate, br',
            #             'Accept-Language': 'zh-CN,zh;q=0.9',
            #             'Upgrade-Insecure-Requests': '1',
            #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,\
            #                      like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            # }
            # try:
            #     url = 'https://www.amazon.com'
            #     proxies = {"https": ip_port}
            #     requests.packages.urllib3.disable_warnings()
            #     s = requests.session()
            #     s.keep_alive = False
            #     request = s.get(url, headers=_header, proxies=proxies)
            #     print(request.status_code)
            #     # print(request.text)
            #     if request.status_code == 200:
            #         print('可用代理' + ip_port)
            #         if IPPool.len_ip() < 30:
            #             IPPool.add_ip(ip_port)
            #         else:
            #             IPPool.rem_ip()
            #             IPPool.add_ip(ip_port)
            #     else:
            #         print('不可用代理' + ip_port)
            # except:
            #     print('不可用代理1' + ip_port)
            time.sleep(self.sleep_time)

    def close(self):
        self.flag = True
        print('closed thread')


if __name__ == '__main__':
    G = GetIpThread('http://api.ip.data5u.com/dynamic/get.html?order=e6913d3978399fbebaf814a6cb554bf8&sep=3', 5.5)
    G.start()
    # time.sleep(5)
    # G.close()
    # G.join()

