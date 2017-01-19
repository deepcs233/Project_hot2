#encoding=utf-8
import json
import random
import jieba
import jieba.analyse
import sys
import pymongo
import math
import time
from basic import Basic
sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings
from utils import repeatability
from  settings import *

colors = ["#33DAB6", "#4BC270", "#C8FF00", "#CC00FF",
          "#AA66CC", "#9933CC", "#00FFFF", "#99CC00", "#669900",
          "#FFBB33", "#FF8800", "#FF4444", "#CC0000"]

with open(PROJECT_PATH+'stopwords.dat','r') as f:
    g=f.readlines()
    
stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

def getRandomXY(range1,range2):
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
class genRG(Basic):

    def __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(genRG,self).__init__(is_last=1,timestamp=timestamp,\
                                      timetuple=timetuple,collection=collection)
        self.graph={"nodes":[],"edges":[]}

    def add_node(self,label,x,y,_id,size):

        #在函数内部完成查重
        for each in self.graph['nodes']:
            if each['id']==label or each['label']==label:
                return
        if label==_id:
            # label 等于　_id 说明是词语,用暖色系
            color=random.choice(WarmColors)
        else:
            color=random.choice(ColdColors)
        
        # 下方的x*2是为了使生成的图更贴合屏幕
        t = {"color":color,"label":label,"x":x*2,"y":y,"id":_id,"size":size}
        self.graph["nodes"].append(t)

    def add_edge(self,node_1,node_2,size=1):
        '''
        node_1 :source node_2:target
        如果node_1 为字符串，则其为soure的label
        '''
        

        if isinstance(node_1,str) or isinstance(node_1,unicode):
            t={"sourceID":node_1,"targetID":node_2,"size":size}
        else:
            t = {"sourceID":node_1["_id"],"targetID":node_2["_id"],"size":size}
        self.graph['edges'].append(t)

    def run(self):
        news_data = []
        words_data = []
        start_time, last_time = self.process_time(column_sort='words_time', collection='words')
        word_dict = self.db['words'].find_one(
            {"$and": [{"words_time": {"$gte": start_time}}, {"words_time": {"$lte": last_time}}]})

        word_dict.pop('_id')
        word_dict.pop('words_time')

        word_tuple = sorted(word_dict.iteritems(), key=lambda x: x[1], reverse=True)[0:50]

        for each in word_tuple:
            words_data.append([each[0], 0])  # 第二个数为该词被引用数
        print words_data[1]
        word_quote_dict = dict(words_data)

        start_time, last_time = self.process_time(column_sort="news_time", collection="news")
        for each_news in self.db['news'].find(
                {"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}). \
                sort('hotxcount', pymongo.DESCENDING).limit(50):

            # 随机选取一部分新闻
            if random.random()<0.5:continue;
            
            news_data.append(each_news)
            x, y = getRandomXY(280, 500)
            self.add_node(label=each_news['news_title'], x=x, y=y,
                          _id=str(each_news['_id']), size=each_news['hot'] / 10)
            text = each_news["news_title"] + each_news["news_body"] + each_news['news_abstract']
 
            words_list = set(jieba.lcut(text))
            news_linked = 0 # 每条新闻已关联的词数
            for each_word in words_list:
                if each_word in word_quote_dict:
                    word_quote_dict[each_word] += 1
                    news_linked += 1
                    if news_linked > MAX_NEWS_LINK_WORD: break
                    self.add_edge(each_word, str(each_news['_id']))

        # 将 {词-引用} 字典按引用数排序
        word_quote_tuple=sorted(word_quote_dict.iteritems(), key=lambda x: x[1], reverse=True)

        for i,word_quote in enumerate(word_quote_tuple):

            if word_quote[1] > 0:
                x,y=getRandomXY(0+i*6,60+i*6)
                print word_quote[0],word_quote[1]
                self.add_node(label=word_quote[0], x=x, y=y,_id=word_quote[0], size=word_dict[word_quote[0]]/7.5)

        with open('graph_index.json','w') as f:
            json.dump(self.graph,f)

        with open(DJANGO_STATIC_PATH+'graph_index.json','w') as f:
            new={}
            new['data']=self.graph
            new['errorMsg']={'errorCode':0,'errorMsg':'success'}
            json.dump(new,f)
            
        return self.graph
                
                
            
if __name__=='__main__':

    start_time=time.clock()
    g=genRG()
    h=g.run()
    end_time=time.clock()
    print 'Time Cost:',end_time
                
