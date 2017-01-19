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

with open(PROJECT_PATH+'stopwords.dat','r') as f:
    g=f.readlines()
stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

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

    def repeatability(self, str_1, str_2, scope):  # 判断字符串Jaccard相似度是否在scope内
        list_1 = set(str_1)
        list_2 = set(str_2)
        a = set(list_1).difference(stopwords)
        b = set(list_2).difference(stopwords)
        intersection = len(a & b)
        union = len(a | b)
        if float(intersection) / union > scope[0] and float(intersection) / union < scope[1]:
            return 1
        else:
            return 0

    def getJaccard(self, str_1, str_2): #计算Jaccard相似度
        list_1 = set(str_1)
        list_2 = set(str_2)
        a = set(list_1).difference(stopwords)
        b = set(list_2).difference(stopwords)
        intersection = len(a & b)
        union = len(a | b)
        return float(intersection) / union

    def jaccard_avg(self,group,avg_threshold=0.25): #计算一个类内的Jaccard平均值是否小于阈值
        length=len(group)
        total_jaccard=[]
        for i in range(length):
            for j in range(i+1,length):
                total_jaccard.append(self.getJaccard(group[i]['title'],group[j]['title']))
        jaccard_avg=sum(total_jaccard)/((length*(length-1))/2)
        if jaccard_avg > avg_threshold:
            return True
        else:
            return False

    def clac_hot(self,data): #计算一个类内新闻的热度(标题新闻热度之和)
        sum_hot = []
        start_time, last_time=self.process_time(column_sort='words_time',collection='words')
        self.word_dict = self.db['words'].find_one({"$and": [{'words_time': {"$gte": start_time}}, {'words_time': {"$lte": last_time}}]})
        for news in data:
            hot = 0
            words = set(jieba.lcut(news['title'])) #集合化，去重，重复的只计算一次
            for word in words:
                hot += self.word_dict.get(word,0)
            hot /= (2+math.sqrt(len(words)))
            sum_hot.append( hot )
        news_hot = sum(sum_hot) / len(sum_hot)
        return news_hot

    def build_dic(self,data): #构建字典，用于存入mangodb
        cluster_dict = {}
        relatedNews = []
        for i in range(1, len(data)):
            related_dict = {}
            related_dict['title'] = data[i]['title']
            related_dict['url'] = data[i]['url']
            relatedNews.append( related_dict )
        hot = self.clac_hot(data)
        cluster_dict['keyNews'] = data[0]['title']
        cluster_dict['relatedNews'] = relatedNews
        cluster_dict['hot'] = hot
        cluster_dict['history_hot'] = [hot]*7
        return cluster_dict

    def run(self):
        data=[]
        start_time, last_time = self.process_time(column_sort='news_time', collection='news')
        for each_news in self.coll.find({"$and":[{"news_time":{"$gte":start_time}},{"news_time":{"$lte":last_time}}]}):
            news={}
            news['title']=each_news['news_title']
            news['url']=each_news['news_url']
            news['flag']=1
            data.append(news)

        for i in range(len(data)):
            #if i%100==0 : print i
            cluster_dict = {}
            new_group = []
            if data[i]['flag']!=1:
                continue
            for j in range(len(data)):
                if data[j]['flag']!=1 or j == i:
                    continue
                if self.repeatability(data[i]['title'],data[j]['title'],(0.24,0.76)):#SCOPE_SIMILAR_NEWS):
                    data[i]['flag']=0
                    data[j]['flag']=0
                    new_group.append(data[i])
                    new_group.append(data[j])
            if len(new_group) > 4 and self.jaccard_avg(new_group):
                cluster_dict = self.build_dic( new_group )
            if cluster_dict != {}:
                #每个聚类保存一次
                self.save( cluster_dict )


    def save(self, cluster_dict, collection='groups'):
        coll_save=self.db[collection]
        cluster_dict['cluster_time'] = time.time()
        coll_save.insert( cluster_dict )


    def update_history_hot(self, collection='group'): #更新历史热度
        for each_news in self.db[collection].find():
            #print each_news['history_hot']
            data = []
            news={}
            news['title'] = each_news['keyNews']
            data.append( news )
            for i in each_news['relatedNews']:
                news = {}
                news['title'] =  i['title']
                data.append( news )
                
            #重新计算hot，改变history_hot的值
            new_hot = self.clac_hot(data)
            history_hot = each_news['history_hot']
            history_hot.pop()
            history_hot.insert(0,new_hot)
            self.db[collection].update({"_id": each_news['_id']}, {'$set': {'history_hot': history_hot}})


if __name__=='__main__':
    f=ClusterNews()
    f.run()
    f.update_history_hot()
