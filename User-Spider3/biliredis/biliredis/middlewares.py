# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# encoding=utf-8
import logging

import scrapy
from scrapy import signals
# from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import random
import requests

import random
from scrapy import signals
from biliredis.settings import IPPOOL


class BiliUserAgentMiddleware():   #UserAgentMiddleware
    '''
    设置随机的User-Agent，

    '''
    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('MY_USER_AGENT')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent
        #print('User-Agent：', agent)




class BiliProxyMiddleware():            #代理池----已经成功，如果失败是代理自身的问题

    def __init__(self, ip=''):

        self.ip = ip

    def process_request(self, request, spider):
        thisip = random.choice(IPPOOL)
        print("this is ip:" + thisip["ipaddr"])
        request.meta["proxy"] = "http://" + thisip["ipaddr"]

# def get_proxy():
#     '''
#     获得代理
#     :return: 可用的代理ip
#     '''
#     return requests.get("http://127.0.0.1:5010/get/").text
#
# class BiliProxyMiddleware():            #代理池----已经成功，但不保证每个代理都可用
#
#     def process_request(self, request, spider):
#         proxy_original = get_proxy()
#         proxy_str = str(proxy_original)
#         proxy = {
#             'http': proxy_str
#         }
#
#         print('代理：', proxy_str)
#         request.meta["proxy"] = "http://" + proxy['http']




    # def process_request(self, request, spider):
    #     thisip = random.choice(IPPOOL)
    #     retry_count = 2
    #     proxy_original = get_proxy()
    #     proxy_str = str(proxy_original)
    #     proxy = {
    #         'http': proxy_str
    #     }
    #     while retry_count > 0:
    #         try:
    #             request.meta["proxy"] = "http://" + proxy['http']
    #         except Exception:
    #             retry_count -= 1
    #
    #             request.meta["proxy"] = "http://" + thisip["ipaddr"]
    #
    #     delete_proxy(proxy)



    # def process_request(self, request, spider):
    #     thisip = random.choice(IPPOOL)
    #     retry_count = 2
    #     proxy_original = get_proxy()
    #     proxy_str = str(proxy_original)
    #     proxy = {
    #         'http': proxy_str
    #     }
    #     while retry_count > 0:
    #         try:
    #             request.meta["proxy"] = "http://" + proxy['http']
    #         except Exception:
    #             retry_count -= 1
    #
    #     delete_proxy(proxy)
    #     return None




    # proxy = self.get_random_proxy()
    # print('当前ip', proxy)
    # if proxy:
    #     uri = 'https://{proxy}'.format(proxy=proxy)
    #     request.meta['proxy'] = uri


    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(proxy_url=settings.get('PROXY_URL'))











# def process_request(self, request, spider):
    #     uri = 'https://127.0.0.1:1087'
    #     print('当前ip', uri)
    #     request.meta['proxy'] = uri

# class RandomUserAgentMiddleware(object):
#     """ 换User-Agent """
#
#     def process_request(self, request, spider):
#         agent = random.choice(agents)
#         request.headers["User-Agent"] = agent





