#coding:utf-8
import re

class Extractor(object):
    def __init__(self, response):
        self.response = response
        self.title = ''
        self.abstract = ''
        self.content = ''

    def execute(self):
        self.getTitle()
        self.getContent()

    def getTitle(self):
        """
        提取当前新闻页面标题

        return:
        - self.title: 字符串，表示标题，可能为空
        """
        title = self.response.xpath('//title/text()').extract()
        if title:
            title = title[0].replace(' ','').replace('\n','').split('_')[0].split('|')[0].split('-')[0]
        self.title = title

    def getContent(self):
        """
        提取当前新闻页面摘要,正文

        return:
        - self.abstract: 字符串，表示新闻摘要，可能为空
        - self.content: 字符串，表示新闻正文，可能为空
        """
        content = self.response.xpath('//p/text()').extract()
        if content:
            x = [self.cleanStr(i) for i in content if len(i.replace(' ','')) > 20]
            s = ''.join(x)
            self.content = s.replace(' ','').replace('\n','').replace('\t','')
            self.abstract = self.getAbst(self.content)

    def getAbst(self, s):
        """
        取新闻正文第一个句号或者问号之前的句子作为新闻摘要

        Input:
        - s: 列表，包含字符串

        Return:
        - abstract: 字符串，表示新闻摘要
        """
        abstract = ''
        for i in s:
            abstract += i
            if i[-1] == u'\u3002' or i[-1] == u'\uff1f':
                break
        return abstract

    def cleanStr(self, s,filter=[]):
        """
        对新闻字符串进行清理，过滤掉无意义词汇

        Input:
        - s: 清理前的字符串
        - filter: 列表，包含要过滤的词语

        Return:
        -s: 清理之后的字符串
        """
        basic_filter = [' ','\n',',',u'\u3000',']','\r']
        basic_filter += filter
        for i in basic_filter:
            s = s.replace(i,'')
        return s
