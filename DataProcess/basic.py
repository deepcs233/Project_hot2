#encoding=utf-8
import pymongo
import time
import sys

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *

class Basic(object):

    def  __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        
        connection=pymongo.MongoClient(MONGODB_HOST,MONGODB_PORT)
        self.db=connection[MONGODB_DATABASE]
        self.coll=self.db[collection]

        if is_last!=1 and timestamp==None and timetuple==None:
            raise(Exception('Time is NULL'))
        self.is_last=is_last
        self.timestamp=timestamp
        self.timetuple=timetuple

    def process_time(self,column_sort="news_time",collection='news',range=1800):
        self.data=[]
        if self.is_last:
            cursor=self.db[collection].find().sort(column_sort,pymongo.DESCENDING)
            last_time=cursor[0][column_sort]
            start_time=last_time-3600 #取最近1800s的区间

        else:
            if self.timetuple !=None:
                newtime=[]
                newtime=list(self.timetuple[0:5])
                newtime+=[0,0,0,0]
                newtime=tuple(newtime)
                start_time=time.mktime(newtime)
                last_time=start_time+1800
            else:
                start_time=self.timestamp
                last_time=self.timestamp+1800

        return start_time,last_time

