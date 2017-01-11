# -*- coding: utf-8 -*-
import scrapy

#清理字符串
def cleanStr(s,filter=[]):
    basic_filter = [' ','\n',',',u'\u3000',']','\r']
##    for i in filter:
##        basic_filter.append(i)
    basic_filter+=filter
    for i in basic_filter:
        s = s.replace(i,'')
    return s

#从字符串中获得摘要
def getStr(s,filter=[]):
    result = ''
    flag = 0
    for i in s:
        for j in filter:
            if j in i:
                flag = 1
                break  # ------改动------
        if flag == 0:
            result += i
        if i[-1] == u'\u3002' or i[-1] == u'\uff1f':
            break
    return result
