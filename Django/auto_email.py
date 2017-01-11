# coding=utf-8
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hot2.settings")# project_name 项目名称
django.setup()
#from django.contrib.auth.models import User
#from monitor.models import UrlsToUser,Update
import requests
import re
from bs4 import BeautifulSoup
import os
from django.core.mail import send_mail
from datetime import timedelta
import logging
from django.core.mail import EmailMessage
from django.template import loader
from hot2.settings import EMAIL_HOST_USER   #项目配置邮件地址，请参考发送普通邮件部分

import time

logging.basicConfig(level=logging.DEBUG,
                    format='<%(levelname)s>%(asctime)s %(filename)s[line:%(lineno)d]  %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='email.log',
                    filemode='a')

SUBJECT=u'网站内容更新！'

def getTitle(text):
    if '/'in text:
        title=text.split('/')[0]
    else:
        title=text
    return title

def timeToStr(time):
    time=time+timedelta(hours=8)
    month=time.month
    day=time.month
    hour=time.hour
    minute=time.minute

    return u'{}月{}日{}时{}分'.format(month,day,hour,minute)



def send_html_mail(subject, content, recipient_list):
    html_content = loader.render_to_string(
                        'mail_template.html',content               #需要渲染的html模板
                        
                   )
    msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, recipient_list)
    with open('11.html','w') as f:
        f.write(html_content.encode('utf-8'))
    msg.content_subtype = "html" 
    msg.send()


send_html_mail('hello',u'你好',['954880786@qq.com'])

##for each_user in User.objects.all():
##    content={}
##    content['number']=0
##    content['newsList']={}
##    receiver=each_user.email
##    content['username']=each_user.username
##    for each_url in UrlsToUser.objects.filter(user=each_user):
##        
##        if len(Update.objects.filter(url=each_url.url))>0:
##            content['number']+=1
##            update=Update.objects.filter(url=each_url.url).order_by('-update_time')[0]
##            title=getTitle(update.content)
##            time=timeToStr(update.update_time)
##            
##            list_=update.content.split('/')[1:]
##            
##            list_=[x.strip() for x in list_]#去除两侧空白字符
##
##            list_=[str(i)+'.'+list_[i-1] for i in range(1,1+len(list_))]#加序号
##            print content['number']
##            
##            content['newsList'][title]={'url':update.url,'time':time,'list':list_}
##            logging.info('Success to email'+receiver)
##
##            
##    try:
##        send_html_mail(SUBJECT, content,[receiver])          
##            
##    except Exception,e:
##            
##        logging.error('Failed to email '+receiver)
##        logging.error(e)

        
    
