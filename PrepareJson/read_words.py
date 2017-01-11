<<<<<<< HEAD
import json

with open('words.json','r') as f:
    words=json.load(f)

for each in words:
    print each
    print '----hot:',words[each]['hot']
    print '----label:',words[each]['label']
    for pj in words[each]['sim']:
        print '----smi_news:',words[each]['sim'][pj]['title']
    print '============'
=======
import json

with open('words.json','r') as f:
    words=json.load(f)

for each in words:
    print each
    print '----hot:',words[each]['hot']
    print '----label:',words[each]['label']
    for pj in words[each]['sim']:
        print '----smi_news:',words[each]['sim'][pj]['title']
    print '============'
>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
