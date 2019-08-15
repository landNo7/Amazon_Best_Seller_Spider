from lxml import etree
import requests

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
    image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Connection': 'close',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'referer': 'https://www.amazon.com/gp/bestsellers',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
     (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}


class GetUrl(object):
    def __init__(self, _depth, _ignore=None, _is_full_page=None, _current_depth=None):
        self.url_list = []
        self.temp_list = []
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

        page = requests.session()
        page.headers = header
        p = page.get(url)
        if self.current_depth == 0:
            print("getting urls... ...")
        # print("https status: %s" % p.status_code)
        xpath = self.xpath_start + self.current_depth * self.xpath_plus + self.xpath_end
        html = etree.HTML(p.text)
        urls = html.xpath(xpath)
        p.close()
        if not urls:
            self.temp_list.append(url)
        elif self.current_depth == self.depth:
            self.temp_list += urls
        else:
            self.current_depth += 1
            for _url in urls:
                # print(_url)
                self.get_url(_url)
            self.current_depth -= 1
        if self.current_depth == 0:
            # if self.is_full_page == 1:  # 爬取前100
            for url_ in self.temp_list:
                self.url_list.append(url_)
                self.url_list.append(url_ + '?_encoding=UTF8&pg=2')
            self.temp_list = []
            print("get urls completed!get {num} url".format(num=len(self.url_list)))

    # 获取分类url列表
    def get_list(self):
        return self.url_list

    # 设置爬虫深度
    def set_depth(self, _depth):
        self.depth = _depth

    # 设置url初始深度
    def set_xpath_start(self, _depth):
        self.xpath_start = self.xpath_start + _depth * self.xpath_plus

    def re_init(self):
        self.xpath_start = '//*[@id="zg_browseRoot"]/ul/ul/'
        self.xpath_plus = 'ul/'
        self.xpath_end = 'li/a/@href'
        self.current_depth = 0

    # 去重
    def rd_list(self):
        temp = list(set(self.url_list))
        temp.sort(key=self.url_list.index)
        self.url_list = temp


if __name__ == '__main__':
    G = GetUrl(2, [], 1)
    G.set_xpath_start(1)
    crawl_list = [
        'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Bar-Tools-Drinkware/zgbs/kitchen/289728/\
        ref=zg_bs_nav_k_1_k',
        'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Wine-Accessories/zgbs/kitchen/13299291/\
        ref=zg_bs_nav_k_1_k',
        'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Utensils-Gadgets/zgbs/kitchen/289754/\
        ref=zg_bs_nav_k_1_k',
        'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Storage-Organization/zgbs/kitchen/510136/\
        ref=zg_bs_nav_k_1_k',
        'https://www.amazon.com/Best-Sellers-Kitchen-Dining-Entertaining/zgbs/kitchen/13162311/\
        ref=zg_bs_nav_k_1_k'
    ]
    for crawl_url in crawl_list:
        G.get_url(crawl_url)
    List = G.get_list()
    print(len(List))
    G.rd_list()
    List = G.get_list()
    print(len(List))
    with open('urls.txt', 'a+') as aw:
        for url in List:
            aw.write(url+'\n')
