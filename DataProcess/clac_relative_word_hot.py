# encoding=utf-8
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

class ClacRelativeFreq(Basic):
    '''
    计算词频相对于上一次的热度
    '''
    def __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(ClacRelativeFreq,self).__init__(is_last=1,timestamp=timestamp,\
                                      timetuple=timetuple,collection=collection)

    def run(self):
        start_time,last_time = self.process_time(column_sort='words_time',collection='words')
        word_dict = list(self.db['words'].find().sort('words_time'))
        
        # 取出最后两个词频字典进行比较
        words_new = word_dict[-1]
        words_old = word_dict[-4]
        word_change = {} 
        
        
        words_sorted = sorted(words_new.iteritems(),key=lambda x:x[1], reverse=True)
        words_old_sorted = sorted(words_old.iteritems(),key=lambda x:x[1], reverse=True)

        # 取旧词频排名的第1000位作为基准
        old_baseline = words_old_sorted[1000][1]
        
        #入选前200个词语 第一个为Object_id,第二个为words_time 故跳过,第三四个为'中国'/'美国',跳过
        for each in words_sorted[4:400]:
            if each[0] in words_old:
                word_change[each[0]] = each[1] / words_old[each[0]]
            else:
                word_change[each[0]] = each[1] / old_baseline
        
            
        return word_change

if __name__ == '__main__':
    t = ClacRelativeFreq()
    f = t.run()
