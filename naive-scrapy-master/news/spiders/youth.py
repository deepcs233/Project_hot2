# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor


class YouthSpider(scrapy.Spider):
    name = "youth"
    def __init__(self):
        self.urlfilter = ['auto','caipiao','photo','video']

    def start_requests(self):
        urls = [
        'http://www.youth.cn/',
        'http://edu.youth.cn/',
        'http://mil.youth.cn/',
        'http://pinglun.youth.cn/',
        'http://health.youth.cn/',
        'http://news.youth.cn/',
        'http://finance.youth.cn/',
        'http://www.youth.cn/',
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
