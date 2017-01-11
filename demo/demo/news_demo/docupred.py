#encoding=utf-8
import jieba
import re
import pickle
from sklearn.svm import SVC
import time
import numpy as np
import math

num_catalog={0:u'财经',1:u'彩票',2:u'房产',3:u'股票',4:u'家居',5:u'教育',
             6:u'科技',7:u'社会',8:u'时尚',9:u'时政',10:u'体育',11:u'星座',
             12:u'游戏',13:u'娱乐'}
             
class classier(object):

    def __init__(self,keywords_file,clf_file,stopwords_file=None):
        '''
        keywords_file 将关键词列表经pickle序列化的文件路径
        stopwords_file 以换行符为分隔的纯文本文件的路径，可以为空
        clf_file 以pkl格式保存的预测模型,调用接口为predict(X)
        '''

        print 'Loading Keywords...'
        try:
            with open(keywords_file,'r') as f:
                self.keywords=pickle.load(f)

        except Exception:
            print '加载关键词文件失败！'



        print 'Loading Stopwords...'
        if stopwords_file==None:
            self.stopwords=None
        else:
            with open(stopwords_file,'r') as f:
                g=f.readlines()
            self.stopwords=[x.rstrip('\n').decode('utf8') for x in g]

        print 'Loading Predict Model...'
        try:
            with open(clf_file,'r') as f:
                self.clf=pickle.load(f)
        
        except Exception:
            print '加载预测模型失败！'
            
    def clac_freq(self,document):

        '''
        传入文本，返回 词-词频 字典
        pat_ch 用于提取出其中的中文字符
        pat_num 用于提取出其中的数字
        pat_en 用于提取中其中的英文单词
        '''      
        pat_num=re.compile(r'\d{2,}')
        pat_en=re.compile(r'[a-zA-Z]{3,}')
        pat_ch=re.compile(u"[\u4e00-\u9fa5]+")
        
        sentences=pat_ch.findall(document)
        ch_text=u''.join(sentences)
        
        word_dict={}
        word_list=[]
        
        word_dict['numOfNumbers']=0

        word_dict['numOfNumbers']+=len(pat_num.findall(document))

        word_list=jieba.lcut(ch_text)
        word_list+=pat_en.findall(document)
        
        if self.stopwords!=None:
            word_list=[x for x in word_list if x not in self.stopwords]#去除停用词，较费时
        
        for word in word_list:
            word_dict.setdefault(word,0)
            word_dict[word]+=1

        return word_dict

    def freq2vec(self,word_dict):
        '''
        此函数将 词-词频 字典转换为向量
        '''

        length=len(self.keywords)
        word2index=dict([(self.keywords[i],i) for i in range(length)])
        new_vec=[0]*length
        
        for word,freq in word_dict.iteritems():
            t=word2index.get(word,None)
            if t==None:
                continue
            else:
                new_vec[t]=freq
        return new_vec
        
    def predict(self,docu,mutilabel=0,threshold=0):

        print 'Start predicting...'
        
        if isinstance(docu,list) or isinstance(docu,tuple):
            self.docuIsList=1
        else:
            self.docuIsList=0


        self.documents=docu
        X_test=[]
        time.clock()
        if self.docuIsList:
            

            for document in self.documents:
                word_dict=self.clac_freq(document)
                vec=self.freq2vec(word_dict)
                X_test.append(vec)
        else:
            word_dict=self.clac_freq(self.documents)
            
            vec=self.freq2vec(word_dict)
            X_test.append(vec)

        if mutilabel:
            tres=self.clf.coef_.dot(np.matrix(X_test).T).T
            
            res=[]
            for i in range(len(tres)):
                t=[]
                chenfen=[]
                tot=0
                for j in range(14):
                    #print tres[i,j],1.3**tres[i,j]
                    hh=1.3**tres[i,j]
                    chenfen.append(hh)
                    tot+=hh
                    
                    if tres[i,j]>threshold:
                        t.append([j,tres[i,j]])
                chenfen=[x/tot for x in chenfen]
                
                t=sorted(t,key=lambda x:x[1],reverse=True)
                res.append(t)
                print chenfen
        else:
            res=self.clf.predict(X_test)
        return res

    def predict_Cn(self,docu,mutilabel=0,threshold=0):
        '''
        预测结果返回中文字符串
        '''
        res=self.predict(docu,mutilabel,threshold)
        res_Cn=[]        
        if isinstance(res[0],int) or isinstance(res[0],float) or isinstance(res[0],np.int64):
            for each in res:
                res_Cn.append(num_catalog[each])
        else:
            
            for i in range(len(res)):
                ans_str=''
                for j in range(len(res[i])):
                    print res[i][j]
                    ans_str=ans_str+' | '+num_catalog[res[i][j][0]]
                ch=str(i+1)+':'+ans_str
                res_Cn.append(ch)
        return res_Cn
            
        
        
if __name__=='__main__':
    
    with open('testnews.txt','r') as f:
        news=f.read().decode('gbk')
    
    cla=classier(keywords_file='keyword_914.pkl',clf_file='logclf.pkl')
    res=cla.predict(docu=news,mutilabel=1,threshold=0)
    print cla.predict_Cn(docu=news,mutilabel=1,threshold=0)

    if isinstance(res[0],int) or isinstance(res[0],float):
        for each in res:
            print num_catalog[each]
    else:
        for i in range(len(res)):
            ans_str=''
            for j in range(len(res[i])):
                ans_str=ans_str+' | '+num_catalog[res[i][j][0]]
            print 'Document'+str(i+1)+':'+ans_str
    print time.clock()
