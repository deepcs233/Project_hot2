# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor

class XinhuaSpider(scrapy.Spider):
    name = "xinhua"
    def __init__(self):
        self.urlfilter = ['auto','house','caipiao','photo','video']

    def start_requests(self):
        urls = [
            'http://www.xinhuanet.com/',
            'http://www.news.cn/politics/',
            'http://www.news.cn/world/index.htm',
            'http://www.news.cn/fortune/',
            'http://www.news.cn/local/index.htm',
            'http://www.news.cn/legal/index.htm',
            'http://www.news.cn/mil/index.htm',
            'http://www.news.cn/sports/',
            'http://ent.news.cn/',
            'http://ent.news.cn/zx.htm',
            'http://ent.news.cn/dy.htm',
            'http://ent.news.cn/ds.htm',
            'http://www.news.cn/politics/xhll.htm',
            'http://www.news.cn/info/',
            'http://www.news.cn/gangao/',
            'http://www.news.cn/tw/',
            'http://www.news.cn/fashion/',
            'http://www.news.cn/tech/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        suffix = ['htm']
        urls = textUrl(response,suffix,self.urlfilter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self,response):
        item = NewsItem()
        ce = Extractor(response)
        ce.execute()
        item['news_title'] = ce.title
        item['news_abstract'] = ce.abstract
        item['news_body'] = ce.content
        item['news_url'] = response.url
        item['news_time'] = time.time()
        yield item
