#encoding=utf-8
import pymongo
import jieba.analyse
import time
import sys
import random
import json
import math
from basic import Basic
from utils import repeatability,normalizeHot

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *

with open(PROJECT_PATH+'stopwords.dat','r') as f:
    g=f.readlines()

stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

LABEL_CHOSEN=[u'财经',u'教育',u'科技',u'社会',u'时尚',u'时政',u'体育']



class genStreamNews(Basic):
    '''
    按每两小时一次生成流式新闻
    '''
    def __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(genStreamNews,self).__init__(is_last=1,timestamp=timestamp,\
                                      timetuple=timetuple,collection=collection)
        self.news=[]
        self.newsGroup=[]
        self.newsStream=[]

        # 获取当前新闻最高热度，便于归一
        # 取最二高的新闻热度作为最高
        # 取最十低的新闻热度作为最低
        start_time,last_time=self.process_time(column_sort='news_time',collection='news')
        self.max_hot=math.sqrt(list(self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}).\
            sort('hotxcount',pymongo.DESCENDING).limit(2))[1]['hotxcount'])
        self.min_hot=math.sqrt(list(self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}).\
            sort('hotxcount',1).limit(10))[9]['hotxcount'])
        
    def getData(self):
        pass

##        待完善
##        start_time,last_time=self.process_time(column_sort='group_time',collection='newsGRoup')
##        for each in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}).\
##            sort('hotxcount',pymongo.DESCENDING).limit(1000):
##            self.news.append(each)



    def getOneLabel(self,label):
        '''
        获取某一分类下的新闻瀑布流
        '''
        #print '='*80
        #print label
        self.news=[]
        self.newsStream=[]
        start_time,last_time=self.process_time(column_sort='news_time',collection='news')
        for each  in self.db['news'].find({"$and":\
                    [{"news_time": {"$gte": start_time}},{"news_time": {"$lte": last_time}},{'label_ch':label}]})\
                    .sort('hotxcount',pymongo.DESCENDING).limit(1000):
            
            self.news.append(each)

        scope=SCOPE_SIMILAR_NEWS

        time_tuple=time.localtime()
        random.seed(int(str(time_tuple[0])+str(time_tuple[1])+str(time_tuple[2])+str(time_tuple[3])))
        news_count=0

        df=[]
        p_threshold=0.4*(1-140.0/len(self.news))
        for i in xrange(len(self.news)):
            #print i,news_count
            t={}
            df.append(math.e**(self.news[i]['hot']/600-0.9))
            if (math.e**(self.news[i]['hot']/600-0.9))*random.random()>p_threshold:
                if news_count>=140: break
                news_count+=1
                
                t['type']='news'
                t['title']=self.news[i]['news_title']
                t['url']=self.news[i]['news_url']
                t['label']=self.news[i]['label_ch']
                t['hot']=normalizeHot(self.news[i]['hotxcount'])

                #print t['hot']
                t['abstract']=self.news[i]['news_abstract']
                t['fromTopic']=self.news[i]['fromTopic']
                text=self.news[i]['news_title']+self.news[i]['news_abstract']+self.news[i]['news_body']
                t['keywords']=jieba.analyse.extract_tags(text,3,allowPOS=('n'))

                start_time,last_time=self.process_time(column_sort='news_time',collection='news')
                t['relatedNews']=[]
                num_sim=NUM_SIMILAR_NEWS2NEWS #相似新闻的选取数量,3
                for each in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, \
                                                           {"news_time": {"$lte": last_time}},\
                                                           {"hot":{"$lte":t['hot']+0.5}}]}).sort('hot',pymongo.DESCENDING).limit(40):
                    if repeatability(each['news_body'],self.news[i]['news_body'],scope) and each['count']!=0:
                        t['relatedNews'].append({
                            'title':each['news_title'],
                            'url':each['news_url'],
                            })
                        num_sim-=1
                        if num_sim<=0:
                            break
                self.newsStream.append(t)

        # 以下插入10组新闻
        start_time,last_time=self.process_time(column_sort='cluster_time',collection='groups')
        for each  in self.db['groups'].find({"$and":\
                    [{"cluster_time": {"$gte": start_time}},{"cluster_time": {"$lte": last_time}},{'label_ch':label}]})\
                    .limit(10):

            t={}
            t['type']='group'
            t['keyNews']=each['keyNews']
            # 只取五则相关新闻
            t['relatedNews']=each['relatedNews'][0:4]
            t['hot']=each['hot']
            t['history']=[]

            # 随机插入
            self.newsStream.insert(int(random.random()*140),t)
            
        #print len(self.news),news_count
        #print sum(df)/len(self.news)

        # 包裹数据
        streamJson={}
        streamJson['errorCode']=0
        streamJson['data']=self.newsStream

        with open('readyStream_'+label+'.json','w') as f:
            json.dump(streamJson,f)

        with open(DJANGO_STATIC_PATH+'readyStream_'+label+'.json','w') as f:

            json.dump(streamJson,f)

    def getAllLabel(self):
        
        self.newsStream=[]
        self.news=[]
        start_time,last_time=self.process_time(column_sort='news_time',collection='news')
        for each in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}).\
            sort('hotxcount',pymongo.DESCENDING).limit(2000):
            self.news.append(each)


                
        scope=SCOPE_SIMILAR_NEWS

        time_tuple=time.localtime()
        random.seed(int(str(time_tuple[0])+str(time_tuple[1])+str(time_tuple[2])+str(time_tuple[3])))
        news_count=0


        for i in xrange(2000):
            #print i,news_count,math.e**(self.news[i]['hot']/600-0.9)
            t={}
            

            if (math.e**(self.news[i]['hot']/700-0.9))*random.random()>0.435:
                
                if news_count>=280: break
                news_count+=1
                t['type']='news'
                t['title']=self.news[i]['news_title']
                t['url']=self.news[i]['news_url']
                t['label']=self.news[i]['label_ch']
                t['hot']=normalizeHot(self.news[i]['hotxcount'])

                #print t['hot']
                t['abstract']=self.news[i]['news_abstract']
                t['fromTopic']=self.news[i]['fromTopic']
                text=self.news[i]['news_title']+self.news[i]['news_abstract']+self.news[i]['news_body']
                t['keywords']=jieba.analyse.extract_tags(text,3,allowPOS=('n'))

                start_time,last_time=self.process_time(column_sort='news_time',collection='news')
                t['relatedNews']=[]
                num_sim=NUM_SIMILAR_NEWS2NEWS #相似新闻的选取数量,3
                for each in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, \
                                                           {"news_time": {"$lte": last_time}},\
                                                           {"hot":{"$lte":t['hot']+0.5}}]}).sort('hot',pymongo.DESCENDING).limit(40):
                    if repeatability(each['news_body'],self.news[i]['news_body'],scope) and each['count']!=0:
                        t['relatedNews'].append({
                            'title':each['news_title'],
                            'url':each['news_url'],
                            })
                        num_sim-=1
                        if num_sim<=0:
                            break
                self.newsStream.append(t)

        
        start_time,last_time=self.process_time(column_sort='cluster_time',collection='groups')
        for each  in self.db['groups'].find({"$and":\
                    [{"cluster_time": {"$gte": start_time}},{"cluster_time": {"$lte": last_time}}]})\
                    .limit(20):

            t={}
            t['type']='group'
            t['keyNews']=each['keyNews']
            # 只取五则相关新闻
            t['relatedNews']=each['relatedNews'][0:4]
            t['hot']=each['hot']
            t['history']=[]

            # 随机插入
            self.newsStream.insert(int(random.random()*280),t)

        # 包裹数据
        streamJson={}
        streamJson['errorCode']=0
        streamJson['data']=self.newsStream

        with open('readyStream.json','w') as f:
            json.dump(streamJson,f)

        with open(DJANGO_STATIC_PATH+'readyStream.json','w') as f:

            json.dump(streamJson,f)

    def run(self):

        for each_label in LABEL_CHOSEN:
            self.getOneLabel(each_label)
        self.getAllLabel()

    def processHot(self,hot):
        '''
        将新闻热度归一为26-100
        保留一位小数
        random添加随机性
        sqrt将热度取根号，使分布尽量均匀
        '''
        if (math.sqrt(hot)) < self.max_hot:
            return round(((math.sqrt(hot)+random.random()-self.min_hot)/(self.max_hot+1-self.min_hot))*74+26,1)
        else:
            return round(98+2*random.random(),1)


if __name__=='__main__':
    
    # 56s
    start_time=time.clock()
    ss=genStreamNews()
    ss.run()
    end_time=time.clock()
    print 'Time Cost:',start_time,end_time
