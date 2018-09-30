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
    #collection = 'users_infomation'

    mid = scrapy.Field()
    # 名字
    name = scrapy.Field()
    # 性别
    sex = scrapy.Field()
    # 生日
    birthday = scrapy.Field()
    # 爬取时间
    crawl_time = scrapy.Field()

    rank = scrapy.Field()

    face = scrapy.Field()
    regtimestamp = scrapy.Field()
    regtime_local = scrapy.Field()
    regtime = scrapy.Field()
    spacesta = scrapy.Field()
    sign = scrapy.Field()
    level = scrapy.Field()
    OfficialVerifyType = scrapy.Field()
    OfficialVerifyDesc = scrapy.Field()
    vipType = scrapy.Field()
    vipStatus = scrapy.Field()
    toutu = scrapy.Field()
    toutuId = scrapy.Field()
    coins = scrapy.Field()

class BiliuserPeople(scrapy.Item):

    mid = scrapy.Field()
    following = scrapy.Field()
    fans = scrapy.Field()

class BiliuserFollower(scrapy.Item):

    # id
    mid = scrapy.Field()
    # 姓名
    uname = scrapy.Field()
    # 头像
    face = scrapy.Field()

