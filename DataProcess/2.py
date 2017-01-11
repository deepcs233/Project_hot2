<<<<<<< HEAD
#encoding=utf-8
import json


with open('stopwords.dat','r') as f:
    g=f.readlines()

stopwords=set([x.rstrip('\n').decode('utf8') for x in g])


with open('sentences.json','r') as f:
    sentences=json.load(f)

sentences=[(x[0],x[1][1]) for x in sentences]

#总词数 9600
with open('words.json','r') as f:
    words=json.load(f)

wordsdict=words
words=sorted(words.iteritems(),key=lambda x: x[1],reverse=True)
words=[(x[0],x[1]) for x in words if words[0] not in stopwords]


##for i in range(100):
##    print words[i][0],words[i][1]

def gen2grams(count,words):
    res=[]
    for i in range(count):
        for j in range(i+1,count):
            res.append([words[i][0],words[j][0],0])
    return res



def countgrams(grams,sentences):
    '''
    用于判断一个二元词组是否会同时出现在一个句子中
    '''
    for sentence in sentences:
        for gram in grams:
            if gram[0] in sentence[0] and gram[1] in sentence[0]:
                gram[2]+=1
    return grams

def countjgrams(grams,sentences):
    '''
    用于判断一个二元词组是否会同时连续的出现在一个句子中
    '''
    for sentence in sentences:
        for gram in grams:
            if gram[0]+gram[1] in sentence[0]:
                gram[2]+=1.0/min(wordsdict[gram[0]],wordsdict[gram[1]])
    
    return grams    

for j in range(400,401,10):
    grams_2=gen2grams(j,words)
    grams_2=countjgrams(grams_2,sentences)
    grams_2=sorted(grams_2,key=lambda x:x[2],reverse=True)

    mean=[]
    for i in range(100):
        mean.append(grams_2[i][2])
        print grams_2[i][0],grams_2[i][1],grams_2[i][2]
    print j,float(sum(mean))/len(mean)
=======
#encoding=utf-8
import json


with open('stopwords.dat','r') as f:
    g=f.readlines()

stopwords=set([x.rstrip('\n').decode('utf8') for x in g])


with open('sentences.json','r') as f:
    sentences=json.load(f)

sentences=[(x[0],x[1][1]) for x in sentences]

#总词数 9600
with open('words.json','r') as f:
    words=json.load(f)

wordsdict=words
words=sorted(words.iteritems(),key=lambda x: x[1],reverse=True)
words=[(x[0],x[1]) for x in words if words[0] not in stopwords]


##for i in range(100):
##    print words[i][0],words[i][1]

def gen2grams(count,words):
    res=[]
    for i in range(count):
        for j in range(i+1,count):
            res.append([words[i][0],words[j][0],0])
    return res



def countgrams(grams,sentences):
    '''
    用于判断一个二元词组是否会同时出现在一个句子中
    '''
    for sentence in sentences:
        for gram in grams:
            if gram[0] in sentence[0] and gram[1] in sentence[0]:
                gram[2]+=1
    return grams

def countjgrams(grams,sentences):
    '''
    用于判断一个二元词组是否会同时连续的出现在一个句子中
    '''
    for sentence in sentences:
        for gram in grams:
            if gram[0]+gram[1] in sentence[0]:
                gram[2]+=1.0/min(wordsdict[gram[0]],wordsdict[gram[1]])
    
    return grams    

for j in range(400,401,10):
    grams_2=gen2grams(j,words)
    grams_2=countjgrams(grams_2,sentences)
    grams_2=sorted(grams_2,key=lambda x:x[2],reverse=True)

    mean=[]
    for i in range(100):
        mean.append(grams_2[i][2])
        print grams_2[i][0],grams_2[i][1],grams_2[i][2]
    print j,float(sum(mean))/len(mean)
>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
