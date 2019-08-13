from lxml import etree
import requests

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


class GetUrl(object):
    def __init__(self, _base_url, _depth, _ignore=None, _is_full_page=None, _current_depth=None):
        self.url_list = []
        self.base_url = _base_url
        self.depth = _depth
        self.ignore = _ignore
        self.is_full_page = _is_full_page
        if _current_depth is None:
            self.current_depth = 0
        else:
            self.current_depth = _current_depth
        self.xpath_start = '//*[@id="zg_browseRoot"]/ul/ul/'
        self.xpath_plus = 'ul/'
        self.xpath_end = 'li/a/@href'

    def get_url(self, url):
        if self.current_depth == 0:
            print("getting urls... ...")
        page = requests.session()
        page.headers = header
        xpath = self.xpath_start + self.current_depth * self.xpath_plus + self.xpath_end
        html = etree.HTML(page.get(url).text)
        urls = html.xpath(xpath)

        if self.current_depth == self.depth:
            self.url_list += urls
        elif not urls:
            self.url_list.append(url)
        else:
            self.current_depth += 1
            for _url in urls:
                self.get_url(_url)
            self.current_depth -= 1
            if self.current_depth == 0:
                if self.is_full_page == 1:          # 爬取前100
                    temp_list = []
                    for url_ in self.url_list:
                        temp_list.append(url_)
                        temp_list.append(url_+'?_encoding=UTF8&pg=2')
                    self.url_list = temp_list
                print("get urls completed!get {num} url".format(num=len(self.url_list)))

    def get_list(self):
        return self.url_list

    def get_current_depth(self):
        return self.current_depth


if __name__ == '__main__':
    base_url = 'https://www.amazon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden/ref=zg_bs_nav_0'
    depth = 1
    ignore = []
    is_full_page = 1
    G = GetUrl(base_url, depth, ignore, is_full_page)
    G.get_url(base_url)
    List = G.get_list()
    print(len(List))
    for __url in List:
        print(__url)
    print(G.get_current_depth())
