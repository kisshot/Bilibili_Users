# -*-coding:utf8-*-

import requests
import json
import random
import datetime
import time
from multiprocessing.dummy import Pool as ThreadPool
import pymongo
from config import *

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

def get_proxy():
    '''
    获得代理
    :return: 可用的代理ip
    '''
    return requests.get("http://127.0.0.1:5010/get/").text              #用.text返回91.121.208.196:3128，而不用.content//.content返回的是b'120.78.51.155:3128',不好处理

proxies = {
    'http': 'http://127.0.0.1:1087'#http://89.43.6.114:8080',
    #'http': 'http://120.52.32.46:80',
    #'http': 'http://218.85.133.62:80',
 }

def LoadUserAgents(uafile):
    useragents = []
    with open(uafile, 'rb') as uaf:
        for useragent in uaf.readlines():
            if useragent:
                useragents.append(useragent.strip()[1:-1 - 1])
    random.shuffle(useragents)
    return useragents

useragents = LoadUserAgents("user_agents.txt")

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
    mid = url.replace('https://space.bilibili.com/', '')
    data = {
        '_': datetime_to_timestamp_in_milliseconds(datetime.datetime.now()),
        'mid': mid
    }
    useragent = random.choice(useragents)
    headers = {
        'User-Agent': useragent,
        'Referer': 'https://space.bilibili.com/' + mid + '?from=search&seid=' + str(random.randint(10000, 50000))
    }
    proxy_str = str('http://' + proxy_original)
    proxy = {
        'http': proxy_str
    }

    print(proxy)
    jscontent = requests.session().post('http://space.bilibili.com/ajax/member/GetInfo',headers=headers,data=data,proxies=proxies).text     #proxies=proxies

    try:
        jsDict = json.loads(jscontent)
        statusJson = jsDict['status'] if 'status' in jsDict.keys() else False
        if statusJson == True:
            if 'data' in jsDict.keys():
                jsData = jsDict['data']
                mid = jsData['mid']
                name = jsData['name']
                sex = jsData['sex']
                rank = jsData['rank']
                face = jsData['face']
                regtimestamp = jsData['regtime']
                regtime_local = time.localtime(regtimestamp)
                regtime = time.strftime("%Y-%m-%d %H:%M:%S", regtime_local)
                spacesta = jsData['spacesta']
                birthday = jsData['birthday'] if 'birthday' in jsData.keys() else 'nobirthday'
                sign = jsData['sign']
                level = jsData['level_info']['current_level']
                OfficialVerifyType = jsData['official_verify']['type']
                OfficialVerifyDesc = jsData['official_verify']['desc']
                vipType = jsData['vip']['vipType']
                vipStatus = jsData['vip']['vipStatus']
                toutu = jsData['toutu']
                toutuId = jsData['toutuId']
                coins = jsData['coins']
                print("Succeed get user info: " + str(mid) )
                print(jscontent)
                print(jsData)
                print(mid, name, sex, rank, face, regtime, spacesta, birthday)
                save_to_mongodb(jsData)
                get_following(mid)

            else:
                print('no data now')
        else:
            print("Error: " + url)
    except Exception as e:
        print(e)
        pass

def get_following(mid):
    jscontent = requests.get('https://api.bilibili.com/x/relation/followings?vmid='+ str(mid) +'&pn=1&ps=20&order=desc&jsonp=jsonp').text
    jsdata = json.loads(jscontent)
    print(jsdata['data']['list'][0])
    '''
    在这里再次添加主函数，就可以完成迭代
    '''
    mid_01 = jsdata['data']['list'][0]['mid']          #第一个关注者的mid标号
    url = 'https://space.bilibili.com/' + str(mid_01)  #第一个关注者的url
    getsource(url)                                     #获取第一个关注者的个人信息以及他的关注者，进入循环，得到他的关注者的mid及url
    '''
    设置I的范围从而指定一开始的'用户'
    【这个'用户'信息——————这个用户关注者有谁】——————【这个用户的关注者信息————————关注者的关注者有谁】——————【关注者的关注者的个人信息
    '''

def save_to_mongodb(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('FAIL',result)

def main(url):
    getsource(url)

if __name__ == "__main__":
    pool = ThreadPool(1)
    try:
        results = pool.map(main, urls)
    except Exception as e:
        print(e)

    pool.close()
    pool.join()
