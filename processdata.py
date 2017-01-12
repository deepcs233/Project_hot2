
#encoding=utf-8
import time

from  DataProcess import clac_word_freq,clac_news_hot,classify_news,rm_samenews,hot_muti_count

from PrepareJson import gen_basic_json,relatedGraph,stream_news
st=time.time()

#3s
a = clac_word_freq.CalcFreq()
a.run()

print time.time()-st
st=time.time()

#5s
b=clac_news_hot.CalcNewsHot()
b.run()

print time.time()-st
st=time.time()

#99s
c=classify_news.newsClassier()
c.run()

print time.time()-st
st=time.time()

#75s
d=rm_samenews.Deduplication()
d.run()

print time.time()-st
st=time.time()

#5s
e=hot_muti_count.CalcNewsHot()
e.run()

#--------------------Prepare JSon-------------------------------


print time.time()-st
st=time.time()

# 85s
f=gen_basic_json.genJsons()
f.prepare_words()


print time.time()-st
st=time.time()

# 4s
f.prepare_news()

print time.time()-st
st=time.time()

# 1s
f.prepare_topics()

print time.time()-st
st=time.time()

# 56s
g=relatedGraph.genRG()
g.run()

print time.time()-st
st=time.time()

# 2s
h=stream_news.genStreamNews()
h.run()

print time.time()-st
st=time.time()


