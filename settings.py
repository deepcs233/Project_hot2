# encoding=utf-8

# Mongodb相关配置
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = "NEWS"
MONGODB_PASSWORD = ""
MONGODB_USERNAME = ""

# Project所在路径
PROJECT_PATH="C:\Users\Administrator\Desktop\project_hot2\\"

# 生成json所存储的路径
JSON_STORE_PATH="C:\Users\Administrator\Desktop\project_hot2\PrepareJson\\"

# 定义新闻相似的Jaccard系数区间
SCOPE_SIMILAR_NEWS=(0.15,0.4)

# 生成news.json时每个新闻所关联的相似新闻数
NUM_SIMILAR_NEWS2NEWS=3

# 生成words.json时每个词语所关联的相似新闻数
NUM_SIMILAR_WORDS2NEWS=3

# 生成topic.json时每个topic相关的新闻数
NUM_TOPICS2NEWS=10

# 在关系图中每条新闻关联的最大词数
MAX_NEWS_LINK_WORD=6

# django静态文件夹路径
DJANGO_STATIC_PATH='c:\Users\Administrator\Desktop\project_hot2\Django\static\\'

# 暖色系 用于热词的配色
WarmColors=['#F41010','#FA5757','#FB2B60','#FF497B','#FF8FBD','#FFA3BA','#F87A7A','#FA9696',\
            '#FDD95C','#FFF76F','#FFCE6F','#FFC092','#FF8755','#FFAC6F','#FF9F82','#FF6D40']

# 冷色系 用于新闻的配色           
ColdColors=['#83DBE4','#6CC5FF','#B69FFF','#5D7EE3','#8B8EF3','#BB7DF6','#7395FF','#72AEF8',]
