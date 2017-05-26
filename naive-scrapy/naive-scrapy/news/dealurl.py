# -*- coding: utf-8 -*-
import pandas as pd
import os
def loadUrls(filepath = 'urls.txt'):
    """
    从文件中读取要爬取的Urls
    """
    urls = pd.read_table(filepath) # 此处路径必须是urls.txt所在的主目录下
    return [urls.iloc[i,0] for i in xrange(len(urls))]

def textUrl(response,suffix,filter, match = ['//li/a','//h2/a','//h3/a']):
    """
    获取当前页面下每条新闻的URL

    Inputs:
    - response:
    - suffix: 符合新闻页面要求的超链接后缀
    - match: 可能出现新闻的标签

    Returns:
    - urls: 列表，可以进一步爬取的url链接
    """
    data = []
    urls = []
    for i in match:
        data += [sel.xpath("text()""|@href").extract() for sel in response.xpath(i)]
    for s in suffix:
        urls += [i for i in data if len(i) == 2 and len(i[1])>9 and s in i[0].split('.')]
    urls = [i[0] for i in urls]
    urls = [url for url in urls if True not in [i in url for i in filter]]
    return urls

def topic(url):
    """
    从Urls中提取能代表类别的关键词
    """
    topicdic = {
                    'news':'时政', 'gov':'时政',
                    'society':'时政', 'world':'时政',
                    'domestic':'时政', 'politics':'时政',
                    'renshi':'时政', 'fanfu':'时政',
                    'theory':'时政',
                    'ent':'娱乐', 'fashion':'娱乐',
                    'tv':'娱乐', 'eladies':'娱乐',
                    'yule':'娱乐',
                    'sports':'体育', 'cba':'体育', 'nba':'体育',
                    'tech':'科技', 'scitech':'科技', 'it':'科技', 'digi':'科技', 'tech':'科技',
                    'money':'财经', 'finance':'财经', 'stock':'财经',
                    'war':'军事', 'mil':'军事', 'military':'军事',
                    'media':'媒体',
                    'gongyi':'公益', 'gy':'公益',
                    'energy':'环保','env':'环保',
                    'culture':'文化', 'health':'文化', 'book':'文化',
                    'games':'游戏',
                }
    topiclist = [topicdic[i] for i in topicdic if i in url]
    if topiclist:
        return topiclist[0]
    else:
        return ''
