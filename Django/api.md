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

## alterUserUrl
POST:
