# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request, FormRequest
import requests
import json
import random

import time
from datetime import datetime
from biliuser.items import BiliuserItem, BiliuserFollower
#from scrapy.http import FormRequest

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['api.bilibili.com','bilibili.com','space.bilibili.com']
    headers = {
        'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Referer': 'https://space.bilibili.com/521401?from=search&seid=' + str(random.randint(10000, 50000))
            #521401
    }
    #

    user_url = 'http://space.bilibili.com/ajax/member/GetInfo'
    follows_url = 'https://api.bilibili.com/x/relation/followings?vmid={user}&pn=1&ps=20&order=desc&jsonp=jsonp'  #521401

    start_user = '521401'

    def start_requests(self):


        #follows_url_2 = 'https://api.bilibili.com/x/relation/followings?vmid=521401&pn=2&ps=20&order=desc&jsonp=jsonp'
        # requests = []
        #formdata= {"mid":"521401"}
        # request = FormRequest(url, callback=self.parse_user, formdata=formdata, headers=self.headers)
        # requests.append(request)

        yield scrapy.http.FormRequest(self.user_url, method='POST', headers=self.headers, formdata={"mid":"521401"}, callback=self.parse_user, dont_filter = True)


        yield scrapy.http.Request(self.follows_url.format(user=self.start_user), callback=self.parse_follows , dont_filter = True)
        #return requests

    def parse_user(self, response):
        print(response.text)

        datas = json.loads(response.text)["data"]

        item = BiliuserItem()
        item["mid"] = datas["mid"]
        item["name"] = datas["name"]
        item["sex"] = datas["sex"]
        item["birthday"] = datas["birthday"]
        item["crawl_time"] = datetime.now()



        mid = str(datas['mid'])

        yield item

        follows_url = self.follows_url.format(user=mid)
        print(follows_url)
        yield scrapy.Request(follows_url, callback=self.parse_follows, dont_filter=True)


    def parse_follows(self, response):

        print(response.text)

        datas = json.loads(response.text)
        if 'data' in datas.keys():
            for data in datas['data']['list']:
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
                                         callback=self.parse_user, dont_filter=True)

                #yield scrapy.Request(follows_url, callback=self.parse_follows, dont_filter=True)
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