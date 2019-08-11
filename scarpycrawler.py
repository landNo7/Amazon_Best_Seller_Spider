from lxml import etree
from bs4 import BeautifulSoup
from lxml import html
import requests
import urllib

header1 = {
    'Accept': 'text/html,application/xhtml+xml, \
                application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '148',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://sso-443.e.buaa.edu.cn',
    'Referer': 'https://sso-443.e.buaa.edu.cn/login',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; \
    Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36',
}

header2 = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;\
    q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://e.buaa.edu.cn',
    'Referer': 'https://e.buaa.edu.cn/users/sign_in',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Mobile Safari/537.36',
}

login_url = 'https://e.buaa.edu.cn/users/sign_in'
login_post_url = 'https://sso-443.e.buaa.edu.cn/login'

page = requests.session()
page.headers = header2


def get_utf8():
    f = page.get(url=login_url)
    soup = BeautifulSoup(f.text, 'lxml')
    utf81 = soup.find('input', {'name': 'utf8'})['value']
    authenticity_token1 = soup.find('meta', {'name': 'csrf-token'})['content']
    return utf81, authenticity_token1


utf8, authenticity_token = get_utf8()
Form_data = urllib.parse.urlencode({
    'utf8': utf8,
    'authenticity_token': authenticity_token,
    'user[login]': 'lqh16061084',
    'user[password]': 'lqh390217',
    'commit': '登录 Login'}).encode("utf-8")

login_url1 = 'https://e.buaa.edu.cn/users/sign_in'

q = page.post(url=login_url1, data=Form_data, headers=header2)

# print(q.text)
#
# 发送登陆请求
#
# ######查看POST请求状态##############
# print(q.url)  # 这句可以查看请求的URL
print(q.status_code)  # 这句可以查看请求状态
# print(q.text)
# for (i,j) in q.headers.items():
#    print(i,':',j)		#这里可以查看响应头
# print('\n\n')
# for (i,j) in q.request.headers.items():
#    print(i,':',j)		#这里可以查看请求头
# 上面的内容用于判断爬取情况，也可以用fiddle抓包查看

# p = page.get('https://e.buaa.edu.cn/')
# print("body", p.text)

wb_data = """
        <div>
            <ul>
                 <li class="item-0"><a href="link1.html">first item</a></li>
                 <li class="item-1"><a href="link2.html">second item</a></li>
                 <li class="item-inactive"><a href="link3.html">third item</a></li>
                 <li class="item-1"><a href="link4.html">fourth item</a></li>
                 <li class="item-0"><a href="link5.html">fifth item</a>
                    <table id = "test" class = "item">test22</table>
             </ul>
         </div>
        """
html = etree.HTML(wb_data)
# print(html)
# result = etree.tostring(html)
# print(result.decode("utf-8"))
html_data = html.xpath('//*[@id="test"]/text()')
print(html_data)
# for i in html_data:
#     print(i.xpath('//text()'))
