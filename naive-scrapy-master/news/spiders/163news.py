# -*- coding: utf-8 -*-
import scrapy
from news.items import NewsItem
from news.dealstr import cleanStr,getStr
from news.dealurl import getUrl,filterUrl
import time

class _163newsSpider(scrapy.Spider):
    name = "163"
    allowed_domains = ["163.com"]
    start_urls = [
    "http://www.163.com",
    ]

    def parse(self, response):
        match1 = '//*[@id="spWrapperHead"]/div[1]/div[2]/div/a/@href'
        match2 = '//*[@id="spWrapperHead"]/div[1]/div[2]/div/strong/a/@href'
        urls = getUrl(response, match1, match2, self.filter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse2)

    def parse2(self, response):
        #li
        data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//li/a')]
        data = [i for i in data if len(i) == 2 and len(i[1])>9 and 'html' in i[0].split('.')]
        #h2
        h2_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h2/a')]
        h2_data = [i for i in h2_data if len(i) == 2 and len(i[1])>9 and 'html' in i[0].split('.')]
        for i in h2_data:
            data.append(i)
        #h3
        h3_data = [sel.xpath("text()""|@href").extract() for sel in response.xpath('//h3/a') ]
        h3_data = [i for i in h3_data if len(i) == 2 and len(i[1])>9 and 'html' in i[0].split('.')]
        for i in h3_data:
            data.append(i)
        #url
        urls = [i[0] for i in data]
        filter = ['goal','cai','corp','fa','vhouse','i.money','v.163.com','open']
        urls = filterUrl(urls,filter)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse3)

    def parse3(self,response):
        item = NewsItem()
        #url
        item['news_url'] = response.url
        #title
        title = response.xpath('//title/text()').extract()
        if title != []:
            title = title[0].replace(',','').replace(' ','').replace('\n','')
            title = title.split('_')[0]
            item['news_title'] = title
        else:
            item['news_title'] = ''
        #abstract & body
        abstract = response.xpath('//p/text()').extract()
        if abstract != []:
            x = [cleanStr(i) for i in abstract if len(i.replace(' ','')) > 20]
            if x != []:
                #过滤原标题，汽车广告
                abs_filter = [u'\u539f\u6807\u9898',u'productname']
                item['news_abstract'] = getStr(x,abs_filter)
                s = ''
                for i in x:
                    s += i
                item['news_body'] = s.replace(' ','').replace('\n','').replace('\t','')
            else:
                item['news_abstract'] = title
                item['news_body'] = title
        else:
            item['news_abstract'] = title
            item['news_body'] = title

        #time
        item['news_time'] = time.time()
        yield item
