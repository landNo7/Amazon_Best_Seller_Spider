import json
import redis
# import Requestdef
r = redis.Redis(host='localhost', port=6379)  # host后的IP是需要连接的ip，本地是127.0.0.1或者localhost


# 主ip池
def add_ip(ip):
    r.lpush('Iplist', ip)


# 备用ip池
def add_ips(ip):
    r.lpush('Iplists', ip)


# 备用ip池第一个开始取出
def app_ips():
    i = str(r.lindex('Iplists', 1), encoding='utf-8')
    r.lrem('Iplists', i, num=0)
    return i


def len_ips():
    return r.llen('Iplists')


def len_ip():
    return r.llen('Iplist')


# 第一个开始取出
def app_ip():
    i = str(r.lpop('Iplist'), encoding='utf-8')
    return i


# 获取product item
def get_item():
    item = r.lpop('amazonSpider:items')
    item = json.loads(item)
    return item


# 取出从最后一个开始
def rem_ip():
    i = str(r.rpop('Iplist'), encoding='utf-8')
    return i

