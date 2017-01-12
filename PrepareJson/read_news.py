##<<<<<<< HEAD
# encoding=utf-8
import json
from math import *
import random

with open('news.json','r') as f:
    news=json.load(f)

t=[]
for each in news:
    
    t.append(e**(news[each]['hot']/300-0.9))

print sum(t)
print len(t)

random.seed(12)
##=======
##<<<<<<< HEAD
### encoding=utf-8
##import json
##from math import *
##import random
##
##with open('news.json','r') as f:
##    news=json.load(f)
##
##t=[]
##for each in news:
##    
##    t.append(e**(news[each]['hot']/300-0.9))
##
##print sum(t)
##print len(t)
##
##random.seed(12)
##=======
### encoding=utf-8
##import json
##from math import *
##import random
##
##with open('news.json','r') as f:
##    news=json.load(f)
##
##t=[]
##for each in news:
##    
##    t.append(e**(news[each]['hot']/300-0.9))
##
##print sum(t)
##print len(t)
##
##random.seed(12)
##>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
##>>>>>>> ec858851f2d016edb34191b927edab87571de0b8
