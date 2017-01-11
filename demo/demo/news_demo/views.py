#encoding=utf-8
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse
import requests
import json
import os

import re
import docupred

# Create your views here.

with open('news_demo/words.json','r') as f:
    wordsdict=json.load(f)

with open('news_demo/sentences.json','r') as f:
    sentences=json.load(f)

with open('news_demo/stopwords.dat','r') as f:
    g=f.readlines()
stopwords=set([x.rstrip('\n').decode('utf8') for x in g])

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0'}
extract=re.compile(u"((?:[\u4e00-\u9fa5]+)|(?:\d{2,}))")
def news(request):
    return render(request,'index.html',{})


def postnews(request):

    if request.method=='POST':
        url=request.POST['url']
        content=request.POST['content']
        title=request.POST['title']

        

        sm_news=[]#相似的新闻列表
        if len(title)>4:
            for i in range(len(sentences)):
                if repeatability(title,sentences[i][0]):
                    sm_news.append(sentences[i])
        clf=docupred.classier(keywords_file='news_demo/keyword_914.pkl',clf_file='news_demo/logclf.pkl')      
        if len(content)>40:
            
            str_clf=clf.predict_Cn(content)[0]
        else:
            if len(url)>8:
                text=requests.get(url,headers=headers).text
                docu=''.join(extract.findall(text))
                str_clf=clf.predict_Cn(docu)[0]
            else:
                if len(sm_news)>0:
                    docu=''
                    for i in range(min(len(sm_news),4)):
                        print 'fgdg--'
                        url=sm_news[0][1][0]
                        text=requests.get(url,headers=headers).text
                        docu=docu+''.join(extract.findall(text))
                    str_clf=clf.predict_Cn(docu)[0]
                else:
                    str_clf=u'信息严重不足，无法做出判断！'

            
        return render(request,'result.html',{'sm_news':sm_news,'clf':str_clf})




def repeatability(str_1,str_2): #判断语句是否重复，是则返回1
    list_1=set(str_1)
    list_2=set(str_2)
    
    a=set(list_1).difference(stopwords)
    b=set(list_2).difference(stopwords)

    intersection=len(a&b)
    union=len(a|b)
    print intersection,union


    if  float(intersection)/union>0.125:#0.435
        return 1
    else:
        return 0
