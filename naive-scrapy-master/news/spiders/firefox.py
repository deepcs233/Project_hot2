# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor

class FirefoxSpider(scrapy.Spider):
    name = "firefox"
    def __init__(self):
        self.urlfilter = ['auto','caipiao','photo','video']

    def start_requests(self):
        urls = [
        'http://www.firefoxchina.cn/',
        'http://domestic.firefox.sina.com/',
        'http://world.firefox.sina.com/',
        'http://mil.firefox.sina.com/',
        'http://society.firefox.sina.com/',
        'http://ent.firefox.sina.com/',
        'http://tech.firefox.sina.com/',
        'http://sports.firefox.sina.com/',
        'http://finance.firefox.sina.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        suffix = ['html']
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
