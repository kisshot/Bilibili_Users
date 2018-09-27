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



# class BiliProxyMiddleware():            #代理池----暂时还未成功
#
#     def process_request(self, request, spider):
#         uri = 'https://127.0.0.1:1087'
#         print('当前ip', uri)
#         request.meta['proxy'] = uri


class BiliProxyMiddleware():            #代理池----暂时还未成功
    def __init__(self, proxy_url):
        self.logger = logging.getLogger(__name__)
        self.proxy_url = proxy_url

    def get_random_proxy(self):
        try:
            response = requests.get(self.proxy_url)
            if response.status_code == 200:
                proxy = response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        print('当前ip', proxy)
        if proxy:
            uri = 'https://{proxy}'.format(proxy=proxy)
            request.meta['proxy'] = uri


    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(proxy_url=settings.get('PROXY_URL'))


# class RandomUserAgentMiddleware(object):
#     """ 换User-Agent """
#
#     def process_request(self, request, spider):
#         agent = random.choice(agents)
#         request.headers["User-Agent"] = agent





