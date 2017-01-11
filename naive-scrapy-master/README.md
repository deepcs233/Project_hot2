# naive-scrapy
## 介绍
基于scrapy的爬虫，爬取门户网站新闻标题，新闻链接，新闻摘要，新闻正文，存入MongoDb或者生成csv文件
网站包括：网易，腾讯，新浪，搜狐, 凤凰, 新华
## 运行
爬取一个门户，以爬取网易主页新闻为例：
```bash
scrapy crawl 163
```
一次全部爬取
```bash
scrapy crawlall
```
