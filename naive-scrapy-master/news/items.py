# -*- coding: utf-8 -*-
import scrapy

class NewsItem(scrapy.Item):
    news_title = scrapy.Field()
    news_url = scrapy.Field()
    news_abstract = scrapy.Field()
    news_body = scrapy.Field()
    news_time = scrapy.Field()
