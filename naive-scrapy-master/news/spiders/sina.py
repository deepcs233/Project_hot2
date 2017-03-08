# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor

class SinanewsSpider(scrapy.Spider):
    name = "sina"
    def __init__(self):
        self.urlfilter = ['auto','lottery','astro','photo','edu','video']

    def start_requests(self):
        urls = [
            'http://www.sina.com.cn/',
            'http://news.sina.com.cn/',
            'http://news.sina.com.cn/hotnews/index_weekly.shtml',
            'http://news.sina.com.cn/china/',
            'http://news.sina.com.cn/world/',
            'http://news.sina.com.cn/society/',
            'http://news.sina.com.cn/opinion/',
            'http://gov.sina.com.cn/',
            'http://sports.sina.com.cn/',
            'http://sports.sina.com.cn/nba/',
            'http://sports.sina.com.cn/china/',
            'http://sports.sina.com.cn/global/',
            'http://sports.sina.com.cn/g/premierleague/',
            'http://finance.sina.com.cn/',
            'http://finance.sina.com.cn/stock/',
            'http://finance.sina.com.cn/fund/',
            'http://finance.sina.com.cn/forex/',
            'http://ent.sina.com.cn/',
            'http://ent.sina.com.cn/star/',
            'http://ent.sina.com.cn/film/',
            'http://ent.sina.com.cn/tv/',
            'http://ent.sina.com.cn/zongyi/',
            'http://ent.sina.com.cn/hr/',
            'http://tech.sina.com.cn/',
            'http://mobile.sina.com.cn/',
            'http://tech.sina.com.cn/discovery/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        suffix = ['shtml']
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
