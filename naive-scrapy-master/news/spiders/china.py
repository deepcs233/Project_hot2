# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor


class ChinaSpider(scrapy.Spider):
    name = "china"
    def __init__(self):
        self.urlfilter = ['auto','lottery','astro','video','photo']

    def start_requests(self):
        urls = [
            'http://www.china.com.cn/',
            'http://news.china.com.cn/',
            'http://finance.china.com.cn/',
            'http://finance.china.com.cn/money/',
            'http://finance.china.com.cn/stock/',
            'http://finance.china.com.cn/industry/index.shtml',
            'http://tech.china.com.cn/',
            'http://tech.china.com.cn/it/',
            'http://tech.china.com.cn/internet/s',
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
