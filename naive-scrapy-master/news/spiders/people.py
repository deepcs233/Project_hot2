# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor


class PeopleSpider(scrapy.Spider):
    name = "people"
    def __init__(self):
        self.urlfilter = ['auto','caipiao','photo','video','qgrmdbdh']

    def start_requests(self):
        urls = [
        'http://www.people.cn/',
        'http://world.people.com.cn/',
        'http://finance.people.com.cn/',
        'http://money.people.com.cn/',
        'http://japan.people.com.cn/',
        'http://usa.people.com.cn/',
        'http://opinion.people.com.cn/',
        'http://sports.people.com.cn',
        'http://edu.people.com.cn',
        'http://politics.people.com.cn/GB/1024/index.html',
        'http://it.people.com.cn/GB/243510/index.html',
        'http://energy.people.com.cn/GB/71890/index.html',
        'http://env.people.com.cn/GB/74877/index.html',
        'http://tw.people.com.cn/GB/104510/index.html',
        'http://military.people.com.cn/GB/172467/index.html',
        'http://legal.people.com.cn/GB/188502/index.html',
        'http://society.people.com.cn/GB/136657/index.html',
        'http://scitech.people.com.cn/GB/1057/index.html',
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
