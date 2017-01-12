#encoding=utf-8
import sys
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

    if float(intersection) / union > scope[0] and float(intersection) / union < scope[1]:
        return 1
    else:
        return 0
##=======
###encoding=utf-8
##import sys
##sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings
##from settings import PROJECT_PATH
##
##with open(PROJECT_PATH+'stopwords.dat','r') as f:
##    g=f.readlines()
##stopwords=set([x.rstrip('\n').decode('utf8') for x in g])
##
##
##def repeatability(str_1, str_2, scope):  # 判断字符串Jaccard相似度是否在scope内
##    list_1 = set(str_1)
##    list_2 = set(str_2)
##
##    a = set(list_1).difference(stopwords)
##    b = set(list_2).difference(stopwords)
##
##    intersection = len(a & b)
##    union = len(a | b)
##
##    if float(intersection) / union > scope[0] and float(intersection) / union < scope[1]:
##        return 1
##    else:
##        return 0
##>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
##
