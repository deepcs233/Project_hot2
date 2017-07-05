
#encoding=utf-8
import json

with open('readyStream.json','r') as f:
    st=json.load(f)['data']

i=0
for each in st:
    if i != 3: 
        print '='*80
        print u'序号:',i %30
        
        
        if each['type']=='news':
            continue
            print u'新闻标题:',each['title']
            print u'新闻热度:',each['hot']
            print u'新闻类别:',each['label']
            print u'关键字:',each['keywords'][0],each['keywords'][1],each['keywords'][2]
            print u'摘要:',each['abstract']
            for eac in each['relatedNews']:
                print u'相关新闻:',eac['title']
        else:
            print each['title']
            print each['hot']
            for eac in each['relatedNews']:
                print u'相关新闻:',eac['title']
    i = i+1

        
