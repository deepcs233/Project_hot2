
# api/
## getUserInfo
GET:
    data {
        "username":"string",
        "email":"string",
        "url":[
            'string',
            'string',
            ……
        ],
        "word":[
          'string',
          'string'
        ],
        "label":[
          'string',
          'string'
        ]
    }

## editUserInfo
POST:

    data:{
        "username":"string",
        "password_old":"string",
        "password_new":"string"
    }

## getHotWords
GET:

    data:{
        "string"(word_id):
            {
                "content":"string",
                "hot":int,
                "fromTopic":"string",
                "history":[int ,int ...],
    
            }
        "string"(word_id):
        {
            ...
        }    
        ...
    }

## getHotNews
GET:

    data:{
        "string"(news_id):
            {
                "content":"string",
                "hot":int,
                "fromTopic":"string",
    
            }
        "string"(news_id):
        {
            ...
        }    
        ...
    }

## getHotTopics
GET:

    data:{
        "string"(news_id):
            {
                "content":"string",
                "hot":int,
                "fromNews":"string",
    
            }
        "string"(news_id):
        {
            ...
        }    
        ...
    }

***



# accounts/

### register

```
data:{
  username:"string",
  email:"string",
  password:"string",
}
```

### login

```
data:{
	username:"string",
	password:"string",
}
```

### logout

```
data:{
  username:"string",
}
```

### fgPasswd

```
data:{
  email:"string",
  captcha:int,
  password:"string:,
}
```

### captcha

```
data:{
  email:"string", 
  or / username:"string" 
}
```



### active_user

### getLoginStatus

```
GET

data:{
  errorCode:int
  username:string
  may errorMsg:string
}
```





***

# api/

###	

```

```



### getNewsPage

```
POST
data:{
  page:int，
  type:'string' // [u'所有',u'财经',u'教育',u'科技',u'社会',u'时尚',u'时政',u'体育']
}
```

响应

```
data:{
  [
    type:"news",
    title:string,
    url:string,
    hot:float,
    <!-- 标签 -->
    label:string,
    keywords:[string,string...],
    <!-- 摘要 -->
    abstract:string,
	  fromTopic:string,
  ],
  [
    type:"group",
    keyNews:string,
    relatedNews:[{
        title:'',
        url:''
      }],
    hot:float,
    history:[float,float...],
  ]
}
```

### getGraph

```
GET
```

响应

```

```
