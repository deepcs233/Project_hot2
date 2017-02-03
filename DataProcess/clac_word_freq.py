#encoding=utf-8
import pymongo
import jieba
import time
import sys
import json
import re
from basic import Basic

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *


with open(PROJECT_PATH+'stopwords.dat','r') as f:
    g=f.readlines()

stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

with open(PROJECT_PATH+'idf.json','r') as f:
    idf=json.load(f)

class CalcFreq(Basic):
    def __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(CalcFreq,self).__init__(is_last=1,timestamp=timestamp,\
                                      timetuple=timetuple,collection=collection)
        

    def get_data(self,start_time,last_time):
        for new in self.coll.find({"$and":[{"news_time":{"$gte":start_time}},{"news_time":{"$lte":last_time}}]}
):
                self.data.append(new['news_title'])
        self.data=''.join(self.data)#将各字符串拼接加快分词速度

    def fenci_clac(self):
        word_list=jieba.lcut(self.data)
        
        word_dict={}
        for each in word_list:
            if len(each)>1 and '.' not in each and each not in stopwords and len(re.findall(r'^\d{2,3}$',each))==0:
                word_dict.setdefault(each,0)

                # 使用td-idf词典，若该词未出现过则取默认值19.1
                word_dict[each]+=idf.get(each,19.1)
        self.dict=word_dict

    def save(self,collection='words'):
        coll_save=self.db[collection]
        self.dict['words_time']=time.time()
        coll_save.insert_one(self.dict)

    def run(self,collection='words'):
        
        #搜索新闻的时间区间
        s_time,l_time=self.process_time(column_sort="news_time")
        self.get_data(s_time,l_time)
        self.fenci_clac()
        self.save(collection)
        
        

if __name__=='__main__':
    f=CalcFreq()
    f.run()
