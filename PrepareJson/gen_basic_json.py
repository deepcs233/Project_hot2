#encoding=utf-8
# 本py中的大段注释为暂时不需要的成分
import json
import pymongo
import sys
import re
from basic import Basic
from bson.objectid import ObjectId
import jieba
import random
import math

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings

from settings import *
from utils import repeatability,normalizeHot

catalogs= [u'财经',u'彩票', u'房产', u'股票', u'家居', u'教育',
                u'科技',  u'社会',  u'时尚',  u'时政',  u'体育',  u'星座',
                u'游戏',  u'娱乐']

with open(PROJECT_PATH+'stopwords.dat','r') as f:
    g=f.readlines()
stopwords=set([x.rstrip('\n').decode('utf8') for x in g])



class genJsons(Basic):

    def __init__(self,is_last=1,timestamp=None,timetuple=None,collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(genJsons,self).__init__(is_last=1,timestamp=timestamp,\
                                      timetuple=timetuple,collection=collection)

    def prepare_words(self):
        words={}
        start_time,last_time=self.process_time(column_sort='words_time',collection='words')

        word_dict=self.db['words'].find_one({"$and":[{"words_time":{"$gte":start_time}},{"words_time":{"$lte":last_time}}]})
        
        #入选前100个词语 第一个为Object_id,第二个为words_time 故跳过,第三四个为'中国'/'美国',跳过
        words_sorted=sorted(word_dict.iteritems(),key=lambda x: x[1],reverse=True)[4:104]

        # 对热度进行归一
        max_hot=words_sorted[0][1]
        min_hot=words_sorted[-1][1]
        print max_hot,min_hot
        
        for each in words_sorted:
            print each[1]
            words[each[0]]={
                'hot':round(normalizeHot(each[1],max_hot,min_hot),1),
                'history':[round(each[1],1)],
                'sim':{}
            }

        #准备历史数据
        for each in words.keys():
            s_time,l_time=start_time,last_time
            for i in range(14*6):#取前14天的信息，每天的热度取6次，然后以该平均值作为本天热度
                s_time-=10800#秒 4*3600
                l_time-=10800
                word_dict=self.db['words'].find_one({"$and": [{"words_time": {"$gte": start_time}}, {"words_time": {"$lte": last_time}}]})
                if word_dict==None:
                    words[each]['history'].append(0)
                else:
                    words[each]['history'].append(round(word_dict.get(each[0],0),1))
            words[each]['history'].reverse() #将历史逆序，越新的排在越后


        #准备与该词语相似的新闻
        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
        for each in words.keys():
            num_sim=NUM_SIMILAR_WORDS2NEWS
            for each_news in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}):
                score=0 #评分
                if each in each_news['news_title']:

                    score+=(1.0/len(each_news['news_title']))*3
                score+=float(len(re.findall(each,each_news['news_abstract'])))/len(each_news['news_abstract'])*10
                if score>0.1:
                    num_sim-=1
                    words[each]['sim'][str(each_news['_id'])]={
                        'title':each_news['news_title'],
                        'urls':each_news['news_url'],
                    }
                if num_sim<=0:
                    break

        #准备该词语的所属类
        for each in words.keys():
            labels=[]#用于存放与该词语相关新闻的类别,目前将会填充3个
            news_ids=words[each]['sim'].keys()
            for each_id in news_ids:
                news_found=self.db['news'].find_one({'_id':ObjectId(each_id)}) #ObjectId 将字符串形式的id转换为Mongodb形式的id以查找
                labels.append(news_found['label_ch'])

            if len(labels)>0:
                t_dict={}
                for label in labels:
                    t_dict.setdefault(label,0)
                    t_dict[label]+=1
                words[each]['label']=sorted(t_dict.iteritems(),key=lambda x: x[1],reverse=True)[0][0]
            else:
                words[each]['label']=u'暂无'
                
        # 以下部分将旧格式的words.josn转化        
        words_data=[]

        for content,each_word_dict in words.iteritems():

            t={}
            t['content']=content
            t['hot']=int(each_word_dict['hot'])
            t['label']=each_word_dict['label']
            t['history']=each_word_dict['history']
            words_data.append(t)

        words={}
        words['errorCode']=0
        words['data']=words_data
        
        with open(JSON_STORE_PATH+'words.json','w') as f:
            json.dump(words,f)



    def prepare_news(self):
        scope=SCOPE_SIMILAR_NEWS #相似度在此i区间内的定义为相似
        news={}
        start_time, last_time = self.process_time(column_sort='news_time', collection='news')

        for each_news in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}}]}).sort('hotxcount',pymongo.DESCENDING).limit(50):

            news[str(each_news['_id'])]={}
            t=news[str(each_news['_id'])] #该处改写成t，要不然看上去难受
            t['title']=each_news['news_title']
            t['abstract']=each_news['news_abstract']
            t['url']=each_news['news_url']
            t['label']=each_news['label_ch']
            t['hot']=each_news['hotxcount']
            
            # !-------------------
            t['fromTopic']=each_news['fromTopic']
            t['sim']={}
            
            news_body=each_news['news_body']#新闻正文

##            #计算相似新闻
##            num_sim=NUM_SIMILAR_NEWS2NEWS #相似新闻的选取数量,3
##            for each in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, \
##                                                       {"news_time": {"$lte": last_time}},{"hot":{"$lte":each_news['hot']+0.5}}]}).sort('hot',pymongo.DESCENDING).limit(40):
##                if repeatability(news_body,each['news_body'],scope) and each_news['count']!=0:
##                    t['sim'][str(each['_id'])]={
##                        'title':each['news_title'],
##                        'url':each['news_url'],
##                        }
##                    num_sim-=1
##                    if num_sim<=0:
##                        break
            
        # 以下部分将旧格式的news.josn转化
        news_data=[]

        for _id,each_news_dict in news.iteritems():
            t={}
            t['news_id']=_id
            t['content']=each_news_dict['title']
            t['url']=each_news_dict['url']
            t['label']=each_news_dict['label']
            t['hot']=int(each_news_dict['hot'])

            # !-------------------
            t['fromTopic']=each_news_dict['fromTopic']

            news_data.append(t)

        news={}
        news['data']=news_data
        news['errorCode']=0
        
        with open(JSON_STORE_PATH+'news.json','w') as f:
            json.dump(news,f)

    def prepare_topics(self):

        start_time, last_time = self.process_time(column_sort='words_time', collection='words')
        # dict --> { '中国':3,'动物':1,...}
        all_word_dict = self.db['words'].find_one({"$and": [{"words_time": {"$gte": start_time}}, {"words_time": {"$lte": last_time}}]})
        all_word_dict.pop('_id')
        # 计算出每个词在所有文档的词中出现的频率
        total_word_freq=sum(all_word_dict.values())
        for word in all_word_dict.keys():
            all_word_dict[word]=all_word_dict[word]/total_word_freq

        topics={}
        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
        for each_topic in catalogs:
            topics[each_topic]={
                'sim':{},
                'hot':0,
                'words':[]
            }
            hot_total=0.0
            text='' # text为前该分类下热度前n篇的标题与摘要字符串
            for each in self.db['news'].find({"$and": [{"news_time": {"$gte": start_time}}, {"news_time": {"$lte": last_time}},\
                                                       {"label_ch":each_topic}]}).sort('hotxcount',pymongo.DESCENDING).limit(10):
                topics[each_topic]['sim'][str(each['_id'])]={
                    'title':each['news_title'],
                    'url':each['news_url']
                }
                hot_total+=each['hot']
                text+=each['news_title']
                text+=each['news_abstract']

            topics[each_topic]['hot'] = hot_total / NUM_TOPICS2NEWS

##            # 以下部分计算每个话题中关联度较高的的词语
##            word_list=jieba.lcut(text)
##            word_dict={}
##            total_words=0
##            for each_word in word_list:
##                if each_word not in stopwords and len(each_word)>1:
##                    word_dict.setdefault(each_word,0)
##                    word_dict[each_word]+=1
##                    total_words+=1
##
##            # 计算各个词语在该分类下所出现的频率
##            for word in word_dict.keys():
##                word_dict[word] = word_dict[word] / total_words
##
##            words_in_label=sorted(word_dict.iteritems(),key=lambda x:x[1],reverse=True)
##            words_in_label=[list(x) for x in words_in_label] # 将tuple类型转换为list，方便后续改动
##
##            for i in range(len(words_in_label)):
##                if words_in_label[i][0] in all_word_dict:
##                    words_in_label[i][1]=words_in_label[i][1] / all_word_dict[words_in_label[i][0]]
##                else:
##                    pass
##
##            words_in_label=sorted(words_in_label,key=lambda x:x[1],reverse=True)
##            for  i in range(10):
##                topics[each_topic]['words'].append(words_in_label[i][0])


        # 以下部分将旧格式的news.josn转化

        topics_data=[]

        for topic,each_topic_dict in topics.iteritems():
            t={}
            t['content']=topic
            t['hot']=int(each_topic_dict['hot'])
            t['relatedNews']=[]
            
            for _ , news_dict in each_topic_dict['sim'].iteritems():
                tt={}
                tt['title']=news_dict['title']
                tt['url']=news_dict['url']
                t['relatedNews'].append(tt)
                
            topics_data.append(t)

        topics={}
        topics['data']=topics_data
        topics['errorCode']=0
            

        with open(JSON_STORE_PATH+'topics.json','w') as f:
            json.dump(topics,f)

    def prepare_all(self):
        self.prepare_words()
        self.prepare_news()
        self.prepare_topics()




if  __name__=='__main__':

    f=genJsons()
    f.prepare_words()
    #f.prepare_news()
    #f.prepare_topics()

