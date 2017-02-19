#encoding=utf-8
import json

with open('idf.json') as f:
    g= json.load(f)

g[u'中国']=3

with open('idf.json','w') as f:
    json.dump(g,f)
