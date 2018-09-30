# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request, FormRequest
import requests
import json
import random

import time
from datetime import datetime
from bilitest.items import BiliuserItem, BiliuserFollower, BiliuserPeople
#from scrapy.http import FormRequest

class BilibiliSpider(scrapy.Spider):
    '''
    整个程序的核心在于循环，具体见Onenote的9.26记录
    '''
    name = 'bilibili'
    allowed_domains = ['api.bilibili.com','bilibili.com','space.bilibili.com']
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Referer': 'https://space.bilibili.com/521401?from=search&seid=' + str(random.randint(10000, 50000))
            #521401
    }
    #
    user_url = 'http://space.bilibili.com/ajax/member/GetInfo'
    people_url = 'https://api.bilibili.com/x/relation/stat?vmid={user}&jsonp=jsonp'
    follows_url = 'https://api.bilibili.com/x/relation/followings?vmid={user}&pn=1&ps=20&order=desc&jsonp=jsonp'  #521401


    start_user = '521401'

    def start_requests(self):
        '''
        初始爬取521401
        :return:
        '''


        #follows_url_2 = 'https://api.bilibili.com/x/relation/followings?vmid=521401&pn=2&ps=20&order=desc&jsonp=jsonp'
        # requests = []
        #formdata= {"mid":"521401"}
        # request = FormRequest(url, callback=self.parse_user, formdata=formdata, headers=self.headers)
        # requests.append(request)

        yield scrapy.http.FormRequest(self.user_url, method='POST', headers=self.headers, formdata={"mid":"521401"}, callback=self.parse_user, dont_filter = True)

        yield scrapy.http.Request(self.people_url.format(user=self.start_user), callback=self.parse_people,
                                  dont_filter=True)

        yield scrapy.http.Request(self.follows_url.format(user=self.start_user), callback=self.parse_follows , dont_filter = True)
        #return requests
#https://api.bilibili.com/x/relation/stat?vmid=521401&jsonp=jsonp
    def parse_user(self, response):
        '''
        个人信息
        :param response:
        :return:
        '''
        #print(response.text)
        print('—————用户个人信息——————')

        datas = json.loads(response.text)["data"]          #提取data数据

        item = BiliuserItem()
        item["mid"] = datas["mid"]
        item["name"] = datas["name"]
        item["sex"] = datas["sex"]                  #赋值
        item["birthday"] = datas["birthday"] if 'birthday' in datas.keys() else 'nobirthday'
        #item["crawl_time"] = datetime.now()
        item["rank"] = datas["rank"]
        item["face"] = datas['face']
        item["regtimestamp"] = datas['regtime']
        regtime_local = time.localtime(item['regtimestamp'])
        item['regtime'] = time.strftime("%Y-%m-%d %H:%M:%S", regtime_local)
        item['spacesta'] = datas['spacesta']
        item['sign'] = datas['sign']
        item['level'] = datas['level_info']['current_level']
        item['OfficialVerifyType'] = datas['official_verify']['type']
        item['OfficialVerifyDesc'] = datas['official_verify']['desc']
        item['vipType'] = datas['vip']['vipType']
        item['vipStatus'] = datas['vip']['vipStatus']
        item['toutu'] = datas['toutu']
        item['toutuId'] = datas['toutuId']
        item['coins'] = datas['coins']

        mid = str(datas['mid'])


        yield item

        follows_url = self.follows_url.format(user=mid)                 #关注者的url
        people_url = self.people_url.format(user=mid)
        print(follows_url)

        yield scrapy.Request(follows_url, callback=self.parse_follows, dont_filter=True)    #调用关注者程序，得到这个人的关注者：进入循环

        yield scrapy.Request(self.people_url.format(user=mid), callback=self.parse_people,
                                  dont_filter=True)                                         #调用关注数、粉丝数函数，得到关注数与粉丝数


        print('-----用户个人信息的结尾---------')

    def parse_people(self, response):

        item = BiliuserPeople()
        print('________用户关注数和粉丝数___________')
        datas = json.loads(response.text)["data"]

        item['mid'] = datas['mid']
        item['following'] = datas['following']
        item['fans'] = datas['follower']

        yield item

        print('________数目结束_________')



    def parse_follows(self, response):
        '''
        关注者列表，重点在于'mid'
        :param response:
        :return:
        '''

        #print(response.text)
        print('用户的关注者信息')

        datas = json.loads(response.text)
        if 'data' in datas.keys():
            for data in datas['data']['list']:    #for data in datas['data']['list'][:2]:
                item = BiliuserFollower()
                item['mid'] = data['mid']
                item['uname'] = data['uname']
                item['face'] = data['face']
                middata = {"mid": str(data["mid"])}
                mid = str(data['mid'])
                yield item

                #follows_url = self.follows_url.format(user=mid)
                #print(follows_url)

                yield scrapy.FormRequest(self.user_url, method='POST', headers=self.headers,
                                         formdata=middata,
                                         callback=self.parse_user, dont_filter=True)      #调用用户函数得到这个关注者的个人信息
                #yield scrapy.Request(follows_url, callback=self.parse_follows, dont_filter=True)
                print('该用户关注者信息结束')
        else:
            print('wrong')
        #headers=self.headers,




        # data = datas['data']['list'][0]
        # item = BiliuserFollower()
        # item['mid'] = data['mid']
        # item['uname'] = data['uname']
        # item['face'] = data['face']
        # yield item



        # datas = json.loads(response.text)["data"]
        #
        # item = BiliuserItem()
        # item["mid"] = datas["mid"]
        # item["name"] = datas["name"]
        # item["sex"] = datas["sex"]
        # item["birthday"] = datas["birthday"]
        # item["crawl_time"] = datetime.now()
        # yield item