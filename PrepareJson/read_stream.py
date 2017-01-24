
#encoding=utf-8
import json

with open('readyStream.json','r') as f:
    st=json.load(f)['data']

for each in st:
    print '='*80
    if each['type']=='news':
        print each['title']
        print each['hot']
        print each['label']
        print each['keywords'][0],each['keywords'][1],each['keywords'][2]
        print each['abstract']
        for eac in each['relatedNews']:
            print u'相关新闻:',eac['title']
    else:
        print each['keyNews']
        print each['hot']
        for eac in each['relatedNews']:
            print u'相关新闻:',eac['title']

        
