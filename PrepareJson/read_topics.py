<<<<<<< HEAD
import json

with open('topics.json','r') as f:
    topics=json.load(f)

for each in topics:
    print each
    print '----hot:',topics[each]['hot']
    for yu in topics[each]['words']:
        print '----words:',yu
    for pj in topics[each]['sim']:
        print '----smi_news:',topics[each]['sim'][pj]['title']
    print '============'
=======
<<<<<<< HEAD
import json

with open('topics.json','r') as f:
    topics=json.load(f)

for each in topics:
    print each
    print '----hot:',topics[each]['hot']
    for yu in topics[each]['words']:
        print '----words:',yu
    for pj in topics[each]['sim']:
        print '----smi_news:',topics[each]['sim'][pj]['title']
    print '============'
=======
import json

with open('topics.json','r') as f:
    topics=json.load(f)

for each in topics:
    print each
    print '----hot:',topics[each]['hot']
    for yu in topics[each]['words']:
        print '----words:',yu
    for pj in topics[each]['sim']:
        print '----smi_news:',topics[each]['sim'][pj]['title']
    print '============'
>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
>>>>>>> ec858851f2d016edb34191b927edab87571de0b8
