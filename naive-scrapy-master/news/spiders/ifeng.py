# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor

class IfengSpider(scrapy.Spider):
    name = "ifeng"
    def __init__(self):
        self.urlfilter = ['house','cp.ifeng','v.ifeng','jiu.ifeng', 'auto',
        'tuangou','phtv.ifeng','vip.v','vc.ifeng','fo.ifeng','jiangjia','photo']

    def start_requests(self):
        urls = [
        'http://www.ifeng.com/',
        'http://news.ifeng.com/',
        'http://news.ifeng.com/mainland/',
        'http://news.ifeng.com/world/index.shtml',
        'http://news.ifeng.com/taiwan/index.shtml',
        'http://news.ifeng.com/hongkong/index.shtml',
        'http://news.ifeng.com/mil/index.shtml',
        'http://news.ifeng.com/society/index.shtml',
        'http://finance.ifeng.com/',
        'http://finance.ifeng.com/money/',
        'http://ent.ifeng.com/',
        'http://sports.ifeng.com/',
        'http://fashion.ifeng.com/',
        'http://tech.ifeng.com/',
        'http://tech.ifeng.com/product/',
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
