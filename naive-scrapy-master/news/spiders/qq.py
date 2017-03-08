# -*- coding: utf-8 -*-
import scrapy
import time
from news.items import NewsItem
from news.dealurl import textUrl
from news.extractor import Extractor

class qqnewsSpider(scrapy.Spider):
    name = "qq"
    def __init__(self):
        self.urlfilter = ['auto','v.qq.com','lottery','astro']

    def start_requests(self):
        urls = [
            'http://news.qq.com',
            'http://news.qq.com/world_index.shtml',
            'http://society.qq.com/',
            'http://mil.qq.com/mil_index.htm',
            'http://news.qq.com/l/milite/milgn/list2010122872223.htm',
            'http://news.qq.com/l/milite/zhoubiansaomiao/list2012095132256.htm',
            'http://news.qq.com/l/milite/milhqj/list2010122872321.htm',
            'http://news.qq.com/l/milite/junbei/list2012095132410.htm',
            'http://view.news.qq.com/',
            'http://finance.qq.com/',
            'http://finance.qq.com/hgjj.htm',
            'http://finance.qq.com/jrsc.htm',
            'http://finance.qq.com/gsbd.htm',
            'http://finance.qq.com/fund/',
            'http://finance.qq.com/xinsanban/index.htm',
            'http://stock.qq.com/',
            'http://sports.qq.com/',
            'http://sports.qq.com/nba/',
            'http://sports.qq.com/cba/',
            'http://sports.qq.com/l/cba/CBAlist.htm',
            'http://sports.qq.com/isocce/',
            'http://sports.qq.com/csocce/csl/',
            'http://sports.qq.com/others/',
            'http://tech.qq.com/',
            'http://tech.qq.com/hlwxw.htm',
            'http://tech.qq.com/it.htm',
            'http://gongyi.qq.com/',
            'http://ent.qq.com/',
            'http://ent.qq.com/zt2012/views/index.htm',
            'http://ent.qq.com/star/',
            'http://ent.qq.com/movie/',
            'http://ent.qq.com/tv/',
            'http://fashion.qq.com/',
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
