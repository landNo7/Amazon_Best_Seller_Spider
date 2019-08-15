
import redis
# import Requestdef
r = redis.Redis(host='127.0.0.1', port=6379)  # host后的IP是需要连接的ip，本地是127.0.0.1或者localhost


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


# 取出从最后一个开始
def rem_ip():
    i = str(r.rpop('Iplist'), encoding='utf-8')
    return i


# 检查主ip池
# def act_db():
#     for i in range(int(r.llen('Iplist')/2)):
#         Requestdef.inspect_ip(rem_ip())
#
#
# # 如果ip池数量少于25个 则填满
# def act_lenip():
#     if r.llen('Iplist') < 25:
#         print('填ip')
#         while r.llen('Iplist') <= 50:
#             Requestdef.inspect_ip(app_ips())
