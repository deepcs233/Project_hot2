# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl, loadUrls, topic
from news.extractor import Extractor

class newsSpider(scrapy.Spider):
    name = "new"
    def __init__(self):
        # 过滤以下不属于新闻的url:汽车广告，彩票，一些专栏
        self.urlfilter = ['auto', 'cai', 'caozhi', 'renjian', 'photoview', 'v.news', 'zajia','miaopai'
                          ,'lottery','astro','video','photo','qgrmdbdh','v.qq.com','edu','house','blog']

    def start_requests(self):
        urls = loadUrls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        获取当前门户主页下每条新闻的URL
        """
        suffix = ['html','shtml','htm']
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
        item['news_updatetime'] = time.time()
        item['news_topic'] = topic(response.url)
        yield item
