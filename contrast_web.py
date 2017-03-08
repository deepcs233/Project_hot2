#encoding=utf-8

import re
import time
import hashlib

import requests
from  bs4 import BeautifulSoup
from bs4 import NavigableString,Comment
import pymongo
from settings import *

RE_CHARSET = re.compile(br'<meta.*?charset=["\']*(.+?)["\'>]', flags=re.I)
RE_PRAGMA = re.compile(br'<meta.*?content=["\']*;?charset=(.+?)["\'>]', flags=re.I)
RE_XML = re.compile(br'^<\?xml.*?encoding=["\']*(.+?)["\'>]')

STR_CLEAN = re.compile(r'[ |\n|\t|\r|<|>]')
MUCH_NUM_OR_EN = re.compile(r'\w{7,}')
EXIST_CH = re.compile(u"[\u4e00-\u9fa5]+")

EXTRACT_GROUP_INFO = re.compile(u'\|([^><]*)\|')

PROCESS_SER_TEXT_1 = re.compile(r'<\|(.*?)\|>')

PROCESS_SER_TEXT_2 = re.compile(r'\|\|')

bad_key=['href','class','blank','div','span','javascript','css','px','width','Copyright','_','void','span','<a>','<p>','|']



def testStr(string):
    '''
    用于检测此字符串是否是合法字符串
    '''
    if len(MUCH_NUM_OR_EN.findall(string)) == 0 and len(EXIST_CH.findall(string)) > 0:
        for each in bad_key:
            if each in string:
                return 0
     
        return 1
    else:
        return 0

def cleanStr(string):
    '''
    清除字符串中的空格、换行、括号等字符
    '''
    return STR_CLEAN.sub('',string)

def search(tag,res):

    for each in tag.children:

        if isinstance(each,Comment):
            continue
        
        if isinstance(each,NavigableString):
            if len(each.string) > 1:
                if testStr(each.string):

                    res.append(cleanStr(each.string))
                    res.append('|')
                    
            continue

        if len(each.contents)<=1:
            if each.string is not None:
                if testStr(each.string):
                    res.append(cleanStr(each.string))
                    res.append('|')
        else:
                res.append('<')
                res.append('|')
                search(each,res)
                if res[-2]=='<':
                    res.pop()
                    res.pop()
                else:
                    res.append('|')
                    res.append('>')

def print_change_dict(change_dict):

    if len(change_dict['add']) > 0:
        print u'新增条目:'
        for each in change_dict['add']:
            print '\t',each
            
    if len(change_dict['remove']) > 0:
        print u'删除条目:'
        for each in change_dict['remove']:
            print '\t',each
            
    if len(change_dict['update']) > 0:
        print u'改动条目'
        for old,new in change_dict['update'].iteritems():
            print '{} ---> {}'.format(old,new)

class WebConstrast(object):

    def __init__(self,url,is_first=0,mode=0,collection='webrecord'):
        '''
        若is_first为1，则表明这是第一次抓取该网站数据，不进行历史对比，也不返回记录
        mode==0 ：精确模式，此模式下若网页框架不同则不会进行比较，直接返回
        mode==1：模糊模式，此模式下不要求网页框架不发生变化，
                但只能选择出上一次未出现而这一次出现的语句，不能给出这些原来是是什么，
                也不能给出这些变化的语句是否是新增的
        '''
        connection = pymongo.MongoClient(MONGODB_HOST,MONGODB_PORT)
        self.db = connection[MONGODB_DATABASE]
        self.coll = self.db[collection]
        self.url = url
        self.is_first = is_first
        self.mode = mode

    def download(self):
        r = requests.get(self.url)
        text  = r.text
        declared_encodings = (RE_CHARSET.findall(text)+RE_PRAGMA.findall(text) +RE_XML.findall(text))
        if len(declared_encodings) > 0:
            enc = declared_encodings[0]
        else:
            enc = 'utf-8'
        r.encoding = enc
        return text

    def serialize(self,text):
        '''
        将网页源代码序列化
        '''
        soup = BeautifulSoup(text,'html.parser').body
        res = ['<','|']


        
        #去除
        for each in list(soup.descendants):
            try:
                if each.name == 'script' or each.text == '\n':
                    each.extract()
            
            except :
                pass

        search(soup,res)
        res.append('>')
        text = ''.join(res).encode('utf-8')
        text = PROCESS_SER_TEXT_1.sub(r'|\g<1>|',text)
        text = PROCESS_SER_TEXT_2.sub(r'',text)
        return text

    def contrast_pres(self,text_old,text_new):
        '''
        精确模式下的对比函数
        新旧网页在某一个区块内的数量相等时发生的改动为 ·update·
            若数目不相等，出现的改动为 ·add· 和 ·remove·
        '''
        old_list = []
        new_list = []
        change_dict = {'add':[],'remove':[],'update':{}}
        for each in EXTRACT_GROUP_INFO.findall(text_old):
            old_list.append(each.split('|'))
            # print each.decode('utf-8')
        for each in EXTRACT_GROUP_INFO.findall(text_new):
            new_list.append(each.split('|'))

        for i in range(len(old_list)):

            # 将在第i个区块的旧新闻列表转化为集合
            old_list_set = set(old_list[i])
            # print old_list_set
            
            if len(old_list[i]) == len(new_list[i]):
                for j in range(len(old_list[i])):
                    if new_list[i][j] not in old_list_set:
                        change_dict['update'][old_list[i][j]]=new_list[i][j]

            else:
                new_list_set = set(new_list[i])
                for each in old_list[i]:
                    if each not in new_list_set:
                        change_dict['remove'].append(each)

                for each in new_list[i]:
                    if each not in old_list_set:
                        change_dict['add'].append(each)
                
                        

        return change_dict
    
    def contrast_fuzz(self,text_old,text_new):
        '''
        模糊模式下的对比函数
        '''
        #此处使用set以完成去重，在函数返回时再将其转换成list
        change_dict = {'change':set([])}
        old_list = set(EXIST_CH.findall(text_old))
        new_list = EXIST_CH.findall(text_new)

        for each in new_list:
            if each not in old_list:
                change_dict['change'].add(each)

        change_dict['change'] = list(change_dict['change'])

        return change_dict
                
    def uptateUrl(self,url):
        self.url = url
        
                
    def run(self):
        html = self.download()
        ser_text = self.serialize(html)
        #frm_text 抽象出网页结构 ex:<<>><<><><><>>><>
        frm_text = ''.join(re.findall(r'[<|>]',ser_text))
        
        ser_hash = hash(ser_text)
        frm_hash = hash(frm_text)

        self.ser_hash = ser_hash
        self.frm_hash = frm_hash
        self.ser_text = ser_text

        #print 'html_hash:',ser_hash
        #print 'frm_hash:',frm_hash
                        
        term={}
        term['time'] = time.time()
        term['url'] = self.url
        term['ser_hash'] = ser_hash
        term['frm_hash'] = frm_hash
        term['ser_text'] = ser_text
        term['frm_text'] = frm_text
        
        if self.is_first:
            self.coll.insert_one(term)
        else:
            old_term=self.coll.find_one({'url':self.url})
            
            if old_term==None:
                return {}
            
            if old_term['ser_hash']==ser_hash:
                #网页未发生变化，返回空
                return {}
            
            if self.mode==0:
                #精确模式
                if old_term['frm_hash']==frm_hash:
                    #网页结构发生变化，返回空
                    return {}
                else:
                    change_dict=self.contrast(old_term['ser_text'],ser_text)
                    #待续
            else:
                #模糊模式
                change_dict=self.contrast_fuzz(old_term['ser_text'],ser_text)


            self.coll.remove({'url':self.url})
            self.coll.insert_one(term)
            return change_dict
                


if __name__ =='__main__' :

    url='http://www.163.com'
    wc=WebConstrast(url=url,is_first=1,mode=0)
    wc.run()
    for i in range(1000):

        ser=wc.ser_hash
        frm=wc.frm_hash
        ser_text=wc.ser_text
        start_time=time.time()
        wc.run()
        end_time=time.time()
        #print 'Time Cost:','{:.2f}s'.format(end_time-start_time)
        #print 'At Time:',u'{}时 {}分 {}秒'.format(time.localtime()[3],time.localtime()[4],time.localtime()[5])                                       
        if wc.ser_hash!=ser:
            print u'网页发生变化!!!!!!!!!'
            if wc.frm_hash==frm:
                start_time=time.time()
                print 'At Time:',u'{}时 {}分 {}秒'.format(time.localtime()[3],time.localtime()[4],time.localtime()[5])                        
                change_dict=wc.contrast_pres(ser_text,wc.ser_text)
                print_change_dict(change_dict)
                end_time=time.time()
                print 'Time Cost:','{:.2f}s'.format(end_time-start_time)
                print '----------'*8
        else:
            #print u'网页未发生变化'
            pass
        if wc.frm_hash!=frm:
            #print u'网页结构发生变化!!!!!!!!!!'
            pass
        else:
            #print u'网页结构未发生变化'
            pass
        #print '----------'*8
        time.sleep(30)

