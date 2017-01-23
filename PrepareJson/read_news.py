# encoding=utf-8
import json
from math import *
import random

with open('news.json','r') as f:
    news=json.load(f)

news=news['data']

for each in news:
    print '='*80
    print each['content']
    print each['label']
    print each['hot']
    
