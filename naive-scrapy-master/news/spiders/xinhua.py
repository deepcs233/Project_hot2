# -*- coding: utf-8 -*-
import scrapy


class XinhuaSpider(scrapy.Spider):
    name = "xinhua"
    allowed_domains = ["xinhuanet.com"]
    start_urls = (
        'http://www.xinhuanet.com/',
    )

    def parse(self, response):
        pass
