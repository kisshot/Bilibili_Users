# -*-coding:utf8-*-

import requests
import json
import random
import datetime
import time
from multiprocessing.dummy import Pool as ThreadPool
import pymongo
from config import *
def get_proxy():
    '''
    获得代理
    :return: 可用的代理ip
    '''
    return requests.get("http://127.0.0.1:5010/get/").text              #用.text返回91.121.208.196:3128，而不用.content//.content返回的是b'120.78.51.155:3128',不好处理

def LoadUserAgents(uafile):
    uas = []
    with open(uafile, 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[1:-1 - 1])
    random.shuffle(uas)
    return uas

uas = LoadUserAgents("user_agents.txt")

# proxies = {
#     'http': 'http://39.137.69.7:80'
# }

urls = []

def datetime_to_timestamp_in_milliseconds(d):
    def current_milli_time():
        return int(round(time.time() * 1000))
    return current_milli_time()


for i in range(5214 * 100, 5215 * 100):
    url = 'https://space.bilibili.com/' + str(i)
    urls.append(url)

def getsource(url):
    proxy_original = get_proxy()
    data = {
        '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
        'mid': url.replace('https://space.bilibili.com/', '')
    }
    ua = random.choice(uas)
    headers = {
        'User-Agent': ua,
        'Referer': 'https://space.bilibili.com/' + str(i) + '?from=search&seid=' + str(random.randint(10000, 50000))
    }
    proxy_str = str('http://' + proxy_original)
    proxy = {
        'http': proxy_str
    }
    print(proxy)
    jscontent = requests.session().post('http://space.bilibili.com/ajax/member/GetInfo',headers=headers,data=data,proxies=proxy).text     #proxies=proxies

    try:
        jsDict = json.loads(jscontent)
        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
        if statusJson == True:
            if 'data' in jsDict.keys():
                jsData = jsDict['data']
                mid = jsData['mid']
                name = jsData['name']
                print("Succeed get user info: " + str(mid) )
                print(jscontent)
                print(jsData)
                print(mid)
                print(name)
            else:
                print('no data now')
        else:
            print("Error: " + url)
    except Exception as e:
        print(e)
        pass

if __name__ == "__main__":
    pool = ThreadPool(1)
    try:
        results = pool.map(getsource, urls)
    except Exception as e:
        print(e)

    pool.close()
    pool.join()
