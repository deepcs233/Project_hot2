<<<<<<< HEAD
#encoding=utf-8
import re
import jieba


num2ch={'0':u'零','1':u'一','2':u'二','3':u'三','4':u'四','5':u'五','6':u'六','7':u'七','8':u'八','9':u'九'}



#db=[]

#for i in range(len(sents)):
#    db.append((i,sents[i]))



#db=[(x[0],x[1].decode('gbk')) for x in db]

'''
去除标定符号
'''

subsym=re.compile(u'[！…，。、：；？【】“》《:‘.,?:!@#{}+*]')

#db=[(x[0],subsym.sub(' ',x[1])) for x in db]

#db=[(x[0],x[1].strip()) for x in db]

#db=[x for x in db if len(x[1])>5]

'''
将字符串中的单数字替换成中文
sdwq2fewg -> sdwq^2^fewg
'''

subnum=re.compile(r'(?<!\d)(\d)(?!\d)')
def processONum(string):
    string=subnum.sub(r'^\g<1>^',string)
    t=string.split('^')
    '''
    '经济学家 要防止房地产泡沫 中国需^8^个一线城市'
    '经济学家 要防止房地产泡沫 中国需' ,'8', '个一线城市'
    
    '''
    
    for i in range(len(t)):
        if len(t[i])==1 and t[i] in num2ch.keys():
            t[i]=num2ch[t[i]]
    return ''.join(t)
#db=[(x[0],processONum(x[1])) for x in db]


        
subbracket=re.compile(r'((?:\(.*?\))|(?:\(.{0,3}$))')
#db=[(x[0],subbracket.sub('',x[1])) for x in db]


#for each in db:
#    print each[0],each[1]


def cleanStr(string):
    #接受unicode字符串
    #处理标点
    string=subsym.sub(' ',string)
    #处理括号
    string=subbracket.sub('',string)
    #长度要求
    if len(string)<=5:
        return ''
    else:
        #将单数字转换为中文
        string=subnum.sub(r'^\g<1>^',string)
        t=string.split('^')
        '''
        '经济学家 要防止房地产泡沫 中国需^8^个一线城市'
        '经济学家 要防止房地产泡沫 中国需' ,'8', '个一线城市'
        
        '''
        
        for i in range(len(t)):
            if len(t[i])==1 and t[i] in num2ch.keys():
                t[i]=num2ch[t[i]]
        return ''.join(t).strip()
    

=======
#encoding=utf-8
import re
import jieba


num2ch={'0':u'零','1':u'一','2':u'二','3':u'三','4':u'四','5':u'五','6':u'六','7':u'七','8':u'八','9':u'九'}



#db=[]

#for i in range(len(sents)):
#    db.append((i,sents[i]))



#db=[(x[0],x[1].decode('gbk')) for x in db]

'''
去除标定符号
'''

subsym=re.compile(u'[！…，。、：；？【】“》《:‘.,?:!@#{}+*]')

#db=[(x[0],subsym.sub(' ',x[1])) for x in db]

#db=[(x[0],x[1].strip()) for x in db]

#db=[x for x in db if len(x[1])>5]

'''
将字符串中的单数字替换成中文
sdwq2fewg -> sdwq^2^fewg
'''

subnum=re.compile(r'(?<!\d)(\d)(?!\d)')
def processONum(string):
    string=subnum.sub(r'^\g<1>^',string)
    t=string.split('^')
    '''
    '经济学家 要防止房地产泡沫 中国需^8^个一线城市'
    '经济学家 要防止房地产泡沫 中国需' ,'8', '个一线城市'
    
    '''
    
    for i in range(len(t)):
        if len(t[i])==1 and t[i] in num2ch.keys():
            t[i]=num2ch[t[i]]
    return ''.join(t)
#db=[(x[0],processONum(x[1])) for x in db]


        
subbracket=re.compile(r'((?:\(.*?\))|(?:\(.{0,3}$))')
#db=[(x[0],subbracket.sub('',x[1])) for x in db]


#for each in db:
#    print each[0],each[1]


def cleanStr(string):
    #接受unicode字符串
    #处理标点
    string=subsym.sub(' ',string)
    #处理括号
    string=subbracket.sub('',string)
    #长度要求
    if len(string)<=5:
        return ''
    else:
        #将单数字转换为中文
        string=subnum.sub(r'^\g<1>^',string)
        t=string.split('^')
        '''
        '经济学家 要防止房地产泡沫 中国需^8^个一线城市'
        '经济学家 要防止房地产泡沫 中国需' ,'8', '个一线城市'
        
        '''
        
        for i in range(len(t)):
            if len(t[i])==1 and t[i] in num2ch.keys():
                t[i]=num2ch[t[i]]
        return ''.join(t).strip()
    

>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
