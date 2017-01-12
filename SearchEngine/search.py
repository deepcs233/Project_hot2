#encoding=utf-8
import pymongo
import jieba
import time
import sys
import random
import json

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from basic import Basic
from  settings import *
from utils import repeatability

with open(PROJECT_PATH+'stopwords.dat','r') as f:
    g=f.readlines()

stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

class SearchEngine(Basic):
    def __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1\，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(SearchEngine,self).__init__(is_last=1,timestamp=timestamp,\
                                      timetuple=timetuple,collection=collection)
    def search(self,query):

        # 使用jieba的搜索引擎分词模式
k        word_list=jieba.lcut_for_search(query)


        # 等待被选作关键词的列表，这里copy一下，因为需要改动
        word_list_to_keyword=word_list[:]
        
        start_time,last_time=self.process_time(column_sort='words_time',collection='words')
        word_dict=self.db['words'].find_one({"$and":[{"words_time":{"$gte":start_time}},{"words_time":{"$lte":last_time}}]})
        
        if len(word_list) == 1:
            keyword=word_list[0]
        else:
            
            # 如果包含多个词语，则选择热度最高的那一个，双字的词语优先
            total_length=sum([len(x) for x in word_list])
            if total_length == len(word_list):
                # 全部由单字组成
                pass
            else:
                 # 若不仅由单字组成，则只选出双字
                word_list_to_keyword = [x for x in word_list_to_keyword if len(x)>1]

            word_freq = [(x,word_dict.get(x,0)) for x in word_list_to_keyword]
            
            keyword=sorted(word_freq,key=lambda x:x[1],reverse=True)[0][0]

        print keyword


if __name__ == '__main__':
    ss=SearchEngine()
    ss.search(u'中国很厉害哦')
        
    
                 
            
            
