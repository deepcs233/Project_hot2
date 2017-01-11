# Project-hot2
热气球

## naive-scrapy-master

### 使用方法：在文件夹下运行scrapy crawl all



## DataProcess 文件夹的文件完成对数据的预处理 

* clac_news_hot.py 计算新闻热度
* clac_word_freq.py  计算词语热度
* classify_news.py  分类新闻
* clean_str.py  字符串清理包，被其他程序引用
* hot_muti_count.py  将新闻的热度与count计算，count越高热度越高，count为0的新闻热度也为0，将不再被显示
* rm_samenews.py  将重复的新闻count置0，将其count转移至其中的一条新闻上
* basic 基类，被其他类所继承

## PrepareJson 提供基本的json文件

* gen_basic_json.py 提供基本的json
* relatedGraph.py  关系图的数据json
* read_graph/topics/words.py  用于美观展示生成的json文件



### contrast_web.py 对比网页，返回改动内容

### processdata.py 集成DataProcess 的文件，运行后可以一次生成所有基本数据

### settings.py 存放配置及常数

### utils.py 存放常用函数

### stopwords.dat 停用词表









