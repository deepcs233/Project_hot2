
# api/
## getUserInfo //获取用户基本信息（用户名，邮箱，是否接受推送）
GET:
    data {
        "username":"string",
        "email":"string",
        'acceptPost': int // 0 --> 不接受推送 , 1 -->接受推送
    }

## editUserame //修改用户名
POST:

    'username': str

## editUserMail //修改用户邮箱

POST:

```
'mail':str
```

## editUserAcceptPost //修改用户是否接受推送

POST:

```
'acceptPost': int // 0 --> 不接受推送 , 1 -->接受推送
```



## getWatchList // 返回关注的词语、标签列表

GET:

```
errorCode:int
may errorMsg:string
data:[
	word1,word2,word3 ...
]
```

## addWatchTag // 增加关注内容

POST:

```
data: Tag
```

## addWatchUrl // 增加订阅网站

POST:

```
data:url
```

## delWatchUrl //删除订阅网站

POST:

```
data:url
```

## getWatchUrl //返回订阅网站列表

GET:

```
data:{
  errorCode:int
  may errorMsg:string
  data:[
    url1,url2...
  ]
  }
```



## getWatchThing   //返回订阅内容

GET:

```
data:{
  errorCode:int
  may errorMsg:string
  data:[
    webTitle //'人民网' :[
		{
          date:'xx-xx',
          time:'xx:xx',
          changeList:[
            str1,str2 ...
          ]  
		},
		
		{ // 一共有5个字典，除第一个以外无’time‘字段
          date:'xx-xx', 
          changeList:[
            str1,str2 ...
          ]  
		}		
    ]
  ]
  }
```



## 

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
