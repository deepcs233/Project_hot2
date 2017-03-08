#encoding=utf-8
import pymongo
import time
import sys
from basic import Basic

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *

class RemoveNews(Basic):
    def __init__(self, is_last=1, timestamp=None, timetuple=None, collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(RemoveNews, self).__init__(is_last=1, timestamp=timestamp, \
                                       timetuple=timetuple, collection=collection)
    def run(self):
        '''
        删除十天前的数据
        '''
        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
        start_time -= 10*24*3600
        self.coll.remove({"news_time": {"$lte": start_time}})
