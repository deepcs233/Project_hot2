<<<<<<< HEAD
#encoding=utf-8
import json

with open('readyStream.json','r') as f:
    st=json.load(f)

for each in st:
    print '='*80
    print each['title']
    print each['hot']
    print each['label']
    print each['keywords'][0],each['keywords'][1],each['keywords'][2]
    print each['abstract']
    for eac in each['relatedNews']:
        print u'相关新闻:',eac['title']

        
=======
<<<<<<< HEAD
#encoding=utf-8
import json

with open('readyStream.json','r') as f:
    st=json.load(f)

for each in st:
    print '='*80
    print each['title']
    print each['hot']
    print each['label']
    print each['keywords'][0],each['keywords'][1],each['keywords'][2]
    print each['abstract']
    for eac in each['relatedNews']:
        print u'相关新闻:',eac['title']

        
=======
#encoding=utf-8
import json

with open('readyStream.json','r') as f:
    st=json.load(f)

for each in st:
    print '='*80
    print each['title']
    print each['hot']
    print each['label']
    print each['keywords'][0],each['keywords'][1],each['keywords'][2]
    print each['abstract']
    for eac in each['relatedNews']:
        print u'相关新闻:',eac['title']

        
>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
>>>>>>> ec858851f2d016edb34191b927edab87571de0b8
