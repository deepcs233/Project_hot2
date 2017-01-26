
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
      errorCode:int
      may errorMsg:string
      data:[
        {
        "content":"string",
        "hot":int,
        "label":"string",
        "history":[int ,int ...],
        }
        ……
      ]
    }

## getHotNews
GET:

    data:{
      errorCode:int
      may errorMsg:string
      data:[
        {
          "news_id": "string"
          "content":"string",
          "url":"string",
          "label":"string",
          "hot":int,
          "fromTopic":"string",
        }
      ]
    }


## getHotTopics
GET:

    data:{
      errorCode:int
      may errorMsg:string
      data:[
        {
          "content":"string",
          "hot":int,
          "relatedNews":[
          	{
          	"title":string,
          	"url":string
          	},
          	...
          	]
      }
      ]
    }

***



# accounts/

###	getLoginStatus

```
GET
data:{
  errorCode:int
  username:string
  may errorMsg:string
}
```

### register

```
POST

data:{
  username:"string",
  email:"string",
  password:"string",
}

返回
data: {
  errorCode:int
  may errorMsg:string
}
```

### login

```
POST

data:{
	username:"string",
	password:"string",
}

返回
data: {
  errorCode:int
  may errorMsg:string
}
```

### logout

```
GET

返回
data: {
  errorCode:int
  may errorMsg:string
}
```

### fgPasswd

```
POST

data:{
  email:"string",
  captcha:int,
  password:"string:,
}

返回
data: {
  errorCode:int
  may errorMsg:string
}
```

### captcha

```
POST
data:{
  email:"string",
  or / username:"string"
}

返回
data: {
  errorCode:int
  may errorMsg:string
}
```



### active_user

***

# api/





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
  errorCode:int
  may errorMsg:string
  data:{
    [
    type:"news",
    title:string,
    url:string,
    hot:int,
    <!-- 标签 -->
    label:string,
    keywords:[string,string...],
    <!-- 摘要 -->
    abstract:string,
    fromTopic:string,
    ],
    [
    type:"group",
    title:string,
    relatedNews:[{
      title:'',
      url:''
      }],
    hot:int,
    history:[int,int...],
    keywords:[string,...]
    ]
    }
}
```

### getGraph

```
GET
```

响应

```
data:{
  errorCode:int
  may errorMsg:string
  data:{
    "nodes": [
      {
        "color": "string",
        "label": "string",
        "y": float,
        "x": float,
        "id": "string",
        "size": float
      },
      ……
  }
}
```

### getSearchGraph

```
POST
data:{
  search: 'string'
}
```

响应

```
data:{
  errorCode:int
  may errorMsg:string
  data:{
    "nodes": [
      {
        "color": "string",
        "label": "string",
        "y": float,
        "x": float,
        "id": "string",
        "size": float
      },
      ……
  }
}
```

### getSearchNews

```
POST
data:{
  search: 'string'
  page: 'number'
}
```

响应

```
data: {
  [
    title:string,
    url:string,
    hot:float,
    <!-- 标签 -->
    label:string,
    keywords:[string,string...],
    <!-- 摘要 -->
    abstract:string,
	  fromTopic:string,
  ]
}
```
