#encoding=utf-8
import sys
import math
import random
sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings
from settings import PROJECT_PATH

with open(PROJECT_PATH+'stopwords.dat','r') as f:
    g=f.readlines()
stopwords=set([x.rstrip('\n').decode('utf8') for x in g])


def repeatability(str_1, str_2, scope):  # 判断字符串Jaccard相似度是否在scope内
    list_1 = set(str_1)
    list_2 = set(str_2)

    a = set(list_1).difference(stopwords)
    b = set(list_2).difference(stopwords)

    intersection = len(a & b)
    union = len(a | b)

    # 改为大于等于和小于等于！
    if float(intersection) / union >= scope[0] and float(intersection) / union <= scope[1]:
        return 1
    else:
        return 0

def getJaccard(str_1,str_2):
    list_1 = set(str_1)
    list_2 = set(str_2)

    a = set(list_1).difference(stopwords)
    b = set(list_2).difference(stopwords)

    intersection = len(a & b)
    union = len(a | b)

    return float(intersection) / union

def normalizeHot(hot,max_hot,min_hot):
    '''
    将新闻热度归一为26-100
    保留一位小数
    random添加随机性
    sqrt将热度取根号，使分布尽量均匀
    '''
    max_hot=math.sqrt(max_hot)
    min_hot=math.sqrt(min_hot)
    hot=math.sqrt(hot)
    if hot > max_hot:
        return 100
    elif hot < min_hot:
        return 26
    else:
        return round(((hot+random.random()-min_hot)/(max_hot+1-min_hot))*74+26,1)
