# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor

class _163newsSpider(scrapy.Spider):
    name = "163"
    def __init__(self):
        #过滤以下不属于新闻的url:汽车广告，网易彩票，一些专栏
        self.urlfilter = ['auto', 'cai', 'caozhi', 'renjian', 'photoview', 'v.news', 'zajia']

    def start_requests(self):
        urls = [
            'http://news.163.com',
            'http://news.163.com/domestic/',
            'http://news.163.com/world/',
            'http://news.163.com/shehui/',
            'http://news.163.com/rank/',
            'http://sports.163.com/',
            'http://sports.163.com/nba/',
            'http://sports.163.com/cba/',
            'http://sports.163.com/china/',
            'http://tech.163.com/',
            'http://tech.163.com/smart/',
            'http://ent.163.com/',
            'http://ent.163.com/movie/',
            'http://ent.163.com/music/',
            'http://ent.163.com/tv/',
            'http://money.163.com/',
            'http://money.163.com/stock/',
            'http://money.163.com/fund/',
            'http://money.163.com/finance/',
            'http://money.163.com/chanjing/',
            'http://war.163.com/',
            'http://data.163.com/',
            'http://gov.163.com/',
            'http://gongyi.163.com/',
            'http://media.163.com/',
            'http://biz.163.com/',
            'http://digi.163.com/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        获取当前门户主页下每条新闻的URL
        """
        suffix = ['html']
        urls = textUrl(response,suffix,self.urlfilter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        """
        爬取并保存当前新闻页面下的新闻url、标题、摘要、正文
        """
        item = NewsItem()
        ce = Extractor(response)
        ce.execute()
        item['news_title'] = ce.title
        item['news_abstract'] = ce.abstract
        item['news_body'] = ce.content
        item['news_url'] = response.url
        item['news_time'] = time.time()
        yield item
