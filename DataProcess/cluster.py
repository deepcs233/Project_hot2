#encoding=utf-8
import pymongo
import time
import sys
import jieba
from basic import Basic
import math
import time

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *
from utils import *

class ClusterNews(Basic):
    def __init__(self, is_last=1, timestamp=None, timetuple=None, collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(ClusterNews, self).__init__(is_last=1, timestamp=timestamp, \
                                       timetuple=timetuple, collection=collection)

    def _filter(self,groups):
        res=[]
        
        for each in gropus:
            if len(each)>3:
                res.append(list(each))
                
        groups=res
        res=[]
        for each_group in groups:
            length=len(each_group)
            total_jaccard=[]
            for i in range(length):
                print each_group[i]
                for j in range(i+1,length):
                    total_jaccard.append(getJaccard(each_group[i],each_group[j]))

            jaccard_avg=sum(total_jaccard)/((length*(length-1))/2)
            print '>>>>'
            print '    组内平均jaccard距离:',jaccard_avg
            print '='*80
            if jaccard_avg>0.22:
                res.append(each_group)
                
        return res
            
            
                    
    def run(self):
        data=[]
        groups=[]
        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
        for each_news in self.coll.find({"$and":[{"news_time":{"$gte":start_time}},{"news_time":{"$lte":last_time}}]}):
            news={}
            news['title']=each_news['news_title']
            news['url']=each_news['news_url']
            news['flag']=1
            data.append(news)
        print len(data)
        for i in range(len(data)):
            if i%100==0 : print i
            new_group=set([])
            if data[i]['flag']!=1:
                continue
            #print data[i]['title']
            for j in range(i+1,len(data)):
                if data[j]['flag']!=1:
                    continue
                if repeatability(data[i]['title'],data[j]['title'],(0.24,0.76)):#SCOPE_SIMILAR_NEWS):
                    data[i]['flag']=0
                    data[j]['flag']=0
                    new_group.add(data[i]['title'])
                    new_group.add(data[j]['title'])
            groups.append(new_group)
        
        return groups
                

if __name__=='__main__':
    f=ClusterNews()
    groups=f.run()
    res=f._filter(groups)

