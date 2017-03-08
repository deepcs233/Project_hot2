#encoding=utf-8
import pymongo
import time
import sys
from basic import Basic
import math

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *

class CalcNewsHot(Basic):
    def __init__(self, is_last=1, timestamp=None, timetuple=None, collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(CalcNewsHot, self).__init__(is_last=1, timestamp=timestamp, \
                                       timetuple=timetuple, collection=collection)
    def run(self):

        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
        for news in self.coll.find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}):
            count=news.get('count',0)
            if count!=0: #系数衰减
                count=math.log(count)+1
            hot=news.get('hot',0)
            self.coll.update_one({"_id": news['_id']}, {'$set': {'hotxcount':count*hot}})

if __name__=='__main__':
    f=CalcNewsHot()
    f.run()
    
##=======
###encoding=utf-8
##import pymongo
##import time
##import sys
##from basic import Basic
##import math
##
##sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings
##
##from settings import *
##
##class CalcNewsHot(Basic):
##    def __init__(self, is_last=1, timestamp=None, timetuple=None, collection='news'):
##        '''
##        默认collection为news
##        若is_last=1，则自动选择最新一次爬取的数据
##        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
##        timetuple精确到小时即可
##        timtestamp将向后搜索1800s
##        '''
##        super(CalcNewsHot, self).__init__(is_last=1, timestamp=timestamp, \
##                                       timetuple=timetuple, collection=collection)
##    def run(self):
##        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
##        for news in self.coll.find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}):
##            count=news.get('count',0)
##            if count!=0: #系数衰减
##                count=math.log(count)+1
##            hot=news.get('hot',0)
##            self.coll.update_one({"_id": news['_id']}, {'$set': {'hotxcount':count*hot}})
##
##if __name__=='__main__':
##    f=CalcNewsHot()
##>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
##    f.run()
