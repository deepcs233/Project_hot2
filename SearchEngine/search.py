#encoding=utf-8
import pymongo
import jieba
import time
import sys
import re
import random
import math
import jieba.analyse
import json



sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from basic import Basic
from  settings import *
from utils import *


punctuation=[u'，',u'。',u'？',u'’',u'“',u'.',',','?',
             u'《',u'》',u'……',u'：',u'；',':',';',u'——']

def get_related_score(word_list,text):
    '''
    计算word_list与text的相关性评分
    word_list 是待查询字符串分词后经过处理的词列表
    '''

    score=0
    for each_word in word_list:
        score += len(re.findall(each_word,text))
    score = float(score)/len(text)
    score = score/math.log(len(word_list)+1,2)

    return score
        

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
        self.graph={'nodes':[],'edges':[]}
        
    def add_node(self,label,x,y,_id,size):

        if label==_id:
            # label 等于　_id 说明是词语,用暖色系
            color=random.choice(WarmColors)
        else:
            color=random.choice(ColdColors)
        
        # 下方的x*2是为了使生成的图更贴合屏幕
        t = {"color":color,"label":label,"x":x*2,"y":y,"id":_id,"size":size}
        return t
    
    def getRandomXY(self,range1,range2):
        '''
        返回 (x,y) 距中心(500,500) 的距离属于(range1,range2)的随机坐标
        '''
        x = random.random() * 1000
        y = random.random() * 1000
        while(1):
            if range1<((x-500)**2+(y-500)**2)<range2:
                break
            else:
                x = random.random() * 1000
                y = random.random() * 1000

        return x,y
        
    def analyse(self,query):

        # 使用jieba的搜索引擎分词模式
        word_list = jieba.lcut_for_search(query)

        #过滤标点符号
        word_list = [x for x in word_list if x not in punctuation]
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
            
            # 如果含有非停用词，则取其中的非停用词
            if len([x for x in word_list_to_keyword if x not in stopwords])>0:
                word_list_to_keyword=[x for x in word_list_to_keyword if x not in stopwords]

            word_freq = [(x,word_dict.get(x,0)) for x in word_list_to_keyword]
            
            keyword=sorted(word_freq,key=lambda x:x[1],reverse=True)[0][0]

        return keyword,word_list_to_keyword

    def search_return_list(self,query):
        
        keyword,word_list=self.analyse(query)
        print  keyword,word_list

        start_time, last_time = self.process_time(column_sort='news_time', collection='news')

        news_list=[]

        # 取不重复的新闻
        for each_news in self.coll.find({"$and":[{"news_time":{"$gte":start_time}},{"news_time":{"$lte":last_time}},\
                                                {'count':{'$gt':0}} ]}).sort('hotxcount',-1).limit(800):
            text=each_news['news_title']*10+each_news['news_abstract']*5+each_news['news_body']

            related_score=get_related_score(word_list,text)

            if related_score == 0:continue
            
            score=related_score*math.log(each_news['hotxcount']+1,10)
            #print related_score
            news_list.append([each_news['_id'],score,text])
            

            

        # 按积分排序
        #print news_list[0][1]
        news_list = sorted(news_list,key=lambda x: x[1],reverse=True)[0:10]

        data=[]
        for each in news_list:
            ee=self.coll.find_one({'_id':each[0]})
            t={}
            t['title']=ee['news_title']
            t['url']=ee['news_url']
            t['hot']=int(ee['hotxcount'])
            t['label']=ee['label_ch']
            t['abstract']=ee['news_abstract']
            t['fromTopic']=ee['fromTopic']
            t['keywords']=jieba.analyse.extract_tags(each[2],3,allowPOS=('n'))

            data.append(t)

        return data

    def search_return_graph(self,query):
    
        keyword,word_list=self.analyse(query)

        start_time, last_time = self.process_time(column_sort='news_time', collection='news')

        news_list=[]

        # 取不重复的新闻
        for each_news in self.coll.find({"$and":[{"news_time":{"$gte":start_time}},{"news_time":{"$lte":last_time}},\
                                                {'count':{'$gt':0}} ]}).sort('hotxcount',-1).limit(800):
            text=each_news['news_title']*10+each_news['news_abstract']*5+each_news['news_body']

            related_score=get_related_score(word_list,text)

            if related_score == 0:continue
            
            score=related_score*math.log(each_news['hotxcount']+1,10)
            #print related_score
            news_list.append([str(each_news['_id']),score,each_news['hotxcount'],each_news['news_title']])
            

            

        # 按积分排序
        #print news_list[0][1]
        news_list = sorted(news_list,key=lambda x: x[1],reverse=True)[0:10]

        data={"nodes":[],"edges":[]}

        # 添加节点
        data['nodes'].append(self.add_node(keyword,450+100*random.random(),450+100*random.random()\
                                           ,keyword,100))
        for each in news_list:
            x, y = self.getRandomXY(50, 400)
            data['nodes'].append(self.add_node(each[3],x,y,each[0],each[2]/20))

        # 添加边
        for each in news_list:
            t={"sourceID":each[0],"targetID":keyword,"size":1}
            data['edges'].append(t)



        return data
        

if __name__ == '__main__':

    ss=SearchEngine()
    time.clock()
    news_list=ss.search_return_graph(u'中国')
    print 'Time Cost:',time.clock()
##    for each_news in news_list:
##        print each_news[0]
##        print each_news[3]
##        print '='*80
##        
