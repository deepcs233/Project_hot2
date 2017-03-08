# -*- coding: utf-8 -*-
import csv
import pymongo
from scrapy.conf import settings

class NewsPipeline(object):
    def __init__(self):
        pass
        #with open('news.csv', 'a') as csvfile:
            #spamwriter = csv.writer(csvfile,dialect='excel')
            #spamwriter.writerow(["标题","链接","摘要","正文","时间"])
    def process_item(self, item, spider):
        if len(item['news_title'])>5 and len(item['news_abstract'])>10 and len(item['news_body'])>80 and len(item['news_title']) > 9 :
            with open('news.csv', 'ab') as csvfile:
                spamwriter = csv.writer(csvfile,dialect='excel')

                title = item['news_title'].encode('utf-8')
                url = item['news_url']
                abstract = item['news_abstract'].encode('utf-8')
                body = item['news_body'].encode('utf-8')
                time = item['news_time']

                spamwriter.writerow([title,url,abstract,body,time])
            return item


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        if len(item['news_title']) > 5 and len(item['news_abstract']) > 20 and len(item['news_abstract']) < 140and len(item['news_body']) > 80 and len(
                item['news_title']) > 9 and len(item['news_title']) < 24:
            self.collection.insert(dict(item))
            return item
