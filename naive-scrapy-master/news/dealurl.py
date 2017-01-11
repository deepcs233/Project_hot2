# -*- coding: utf-8 -*-
import scrapy

#Url过滤
def filterUrl(urls,filter):
##    result = []
##    for x in urls:
##        flag = 0
##        for f in filter:
##            if f in x:
##                flag = 1
##                break
##        if flag == 0:
##            result.append(x)
    result=[x for x in urls if x not in filter]
    return result

#提取首页Url
def getUrl(response,match1,match2,filter):
    url_1 = response.xpath(match1).extract()
    url_1.append(response.url)
    if match2 != []:
        url_2 = response.xpath(match2).extract()
        for i in url_2:
            url_1.append(i)
    url_1 = filterUrl(url_1,filter)
    return url_1
