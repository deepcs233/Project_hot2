# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor

class SohunewsSpider(scrapy.Spider):
    name = "sohu"
    def __init__(self):
        self.urlfilter = ['auto','astro','2016.sohu.com','caipiao']

    def start_requests(self):
        urls = [
            'http://www.sohu.com/',
            'http://news.sohu.com/',
            'http://pinglun.sohu.com/',
            'http://news.sohu.com/guoneixinwen.shtml',
            'http://news.sohu.com/shehuixinwen.shtml',
            'http://news.sohu.com/guojixinwen.shtml',
            'http://mil.sohu.com/',
            'http://police.news.sohu.com/',
            'http://sports.sohu.com/',
            'http://sports.sohu.com/guoneizuqiu.shtml',
            'http://sports.sohu.com/lanqiu.shtml',
            'http://sports.sohu.com/zonghe.shtml',
            'http://sports.sohu.com/nba.shtml',
            'http://cbachina.sports.sohu.com/',
            'http://sports.sohu.com/zhongchao.shtml',
            'http://business.sohu.com/',
            'http://soyule.sohu.com/',
            'http://it.sohu.com/',
            'http://fashion.sohu.com/',
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
