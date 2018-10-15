# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import MySQLdb
# import MySQLdb.cursors
import pymysql

from bilitest.items import BiliuserItem, BiliuserFollower, BiliuserPeople, Biliuserfans


class MongoPipeline(object):
    collection_users = 'users_infomation'
    collection_people = 'number_of_fans_followers'
    collection_followers = 'followers_info'
    collection_fans = 'fans_info'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_url = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        if isinstance(item, BiliuserItem):
            self.db[self.collection_users].update({'mid':item.get('mid')}, {'$set':dict(item)}, True)
        # if isinstance(item, BiliuserPeople):
        #     self.db[self.collection_people].update({'mid':item.get('mid')}, {'$set':dict(item)}, True)
        # if isinstance(item, BiliuserFollower):
        #     self.db[self.collection_followers].update({'mid':item.get('mid')}, {'$set':dict(item)}, True)
        # if isinstance(item, Biliuserfans):
        #     self.db[self.collection_fans].update({'mid': item.get('mid')}, {'$set': dict(item)}, True)
        return item

    def close_spider(self, spider):
        self.client.close()





class MysqlDBPipleline(object):
    def __init__(self):
        self.count = 1
        self.conn = pymysql.connect(
            host='localhost',
            port= 3306,
            user='root',
            # 这里填写密码
            passwd='lf9752915',
            db='bilibili',
            charset='utf8',
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, BiliuserItem):
            try:
                print("***********at beginning of saving**********")
                print(dict(item))


                # sql = 'INSERT INTO bilibili_user_info(mid, name, sex) VALUES (%s, %s, %s)'
                #
                # lis = (item['mid'], item['name'], item['sex'])

                # sql = """insert into bilibili_user_info(mid,name,sex) VALUES (%s,%s,%s)""" ,(
                #                 item['mid'], item['name'], item['sex'])

                mid = int(item['mid'])
                name = str(item['name'])
                sex = str(item['sex'])

                self.cursor.execute("insert into bilibili_user_info(mid,name,sex) VALUES (%s,%s,%s)" ,(
                mid,name,sex,))


                self.conn.commit()

            except Exception:
                print('===========ERROR================')
                pass

        return item

    def close_spider(self, spider):
        self.conn.close()
