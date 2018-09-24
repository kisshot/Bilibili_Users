# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiliuserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # id
    mid = scrapy.Field()
    # 名字
    name = scrapy.Field()
    # 性别
    sex = scrapy.Field()
    # 生日
    birthday = scrapy.Field()
    # 爬取时间
    crawl_time = scrapy.Field()

class BiliuserFollower(scrapy.Item):

    # id
    mid = scrapy.Field()
    # 姓名
    uname = scrapy.Field()
    # 头像
    face = scrapy.Field()
