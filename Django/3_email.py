#coding=utf-8
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hot2.settings")# project_name 项目名称
django.setup()
from django.core.mail import send_mail
from django.template import loader
import time
import sys
import pymongo

sys.path.append('../') # 在路径中添加上级目录，方便导入父级目录的settings
from basic import Basic

content = {}

weekDict = {0:u'一', 1:u'二', 2:u'三', 3:u'四', 4:u'五',5:u'六',6:'天'}

colors = ['ff5353', 'ffa869', 'ffdc69', 'c3ed58', '58edcc']

tTuple = time.localtime()
time = {}
time['day'] = u'星期'.encode('utf-8') + weekDict[tTuple[6]]
time['month'] = tTuple[1]
time['date'] = tTuple[2]

content['time'] = time



class ChooseNews(Basic):
    def __init__(self, is_last=1, timestamp=None, timetuple=None, collection='news'):
        '''
        默认collection为news
        若is_last=1，则自动选择最新一次爬取的数据
        若is_last！=1，则接受timestamp或timetuple将在该时间内的数据作为来源
        timetuple精确到小时即可
        timtestamp将向后搜索1800s
        '''
        super(ChooseNews, self).__init__(is_last=1, timestamp=timestamp, \
                                       timetuple=timetuple, collection=collection)
    def run(self):
        start_time, last_time = self.process_time(column_sort='news_time', collection='news')

        yaowenList = []

        i = 0
        for each  in self.db['news'].find({"$and":\
                            [{"news_time": {"$gte": start_time}},{"news_time": {"$lte": last_time}}]})\
                            .sort('hotxcount',pymongo.DESCENDING).limit(5):
            t = {}
            t['title'] = each['news_title']
            t['color'] = colors [i]
            t['url'] = each['news_url']

            yaowenList.append(t)
            i += 1
        return yaowenList

cn = ChooseNews()
content['yaowen'] = cn.run()

html_content = loader.render_to_string(
                        'email.html',content               #需要渲染的html模板
                        
                   )
#1942037006
send_mail('Subject here', 'Here is the message.', 'dailynews@hottestdaily.com',
    ['954880786@qq.com'], fail_silently=False,html_message = html_content)
