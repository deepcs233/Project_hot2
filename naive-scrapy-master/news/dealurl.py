# -*- coding: utf-8 -*-

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
