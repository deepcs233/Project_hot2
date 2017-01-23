import json

with open('topics.json','r') as f:
    topics=json.load(f)
    
topics=topics['data']
    
for each in topics:
    print each['content']
    print '----hot:',topics[each]['hot']

    for pj in each['relatedNews']:
        print '----related_news:',pj['title']
    print '============'

