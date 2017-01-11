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
        ]
<<<<<<< HEAD
        "label":[
          string,
          ...
        ]
        "word":[
          string,
          ...
        ]
=======
>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
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

<<<<<<< HEAD


=======
>>>>>>> eee6113b95b6f94b795bbd3ec39a0625545043ad
### logout

```
data:{
  username:"string",
}
```

### fgPasswd

```
data:{
  username:"string",
  captcha:int,
}
```

### active_user

***

# api/

### getNewsPage

```
GET
data:{
  page:int
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
    label:string,
    keywords:[string,string...],
    abstract:string,
	fromTopic:string,
	relatedNews:[string,url,string,url...],
  ],
  [
    type:"group",
    keyNews:string,
    relatedNews:[string,url,string,url...],
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



### postUserClick

```
POST
data:{
  _id=string
}
```



### search

```
POST
data:{
  c:string
}
```



Response:







