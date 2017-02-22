prefix=/v1/bbs

统一回复格式:
```
{
    error_code: 0 // 0 成功, >0 错误
    message: "xxx" // 空字符 或者 错误信息
    data: JSONObj, // 可能为json对象或者json数组
}
```

对象格式:

论坛简单信息
```
SimpleForum
{
    id: 123,
    name: "火影",
    cover: "http://full-url.jpg"
    today_cnt: 12,
    total_cnt: 1024,
}
```

Feed简单信息
```
SimpleFeed
{
    id: 123,
    title: "标题",
    cover: "http://full-url.jpb",
    reply_cnt: 5 // 回复个数
    author_name: "作者名称",
    forum_name: "板块名称",
    created_at: 14xxxxxx, // unix时间戳
}
```


1. 根据ID取得游戏信息和板块信息

```
GET forum/{id} 
response:
{
    {{SimpleForum}}
    sub_forum: [
        {{SimpleForum}}, 
        ...
    ]
}
```

2. 根据userid获取所关注游戏信息

```
GET following/forums
response:
[
    {{SimpleForum}},
    ...
]
```

3. 获取论坛的Feed流

```
GET forum/{id}/feed
request:
{
    type: 0, // 0 - 推荐，1-【最新】， 2-【回复】
    start: 0 //分页用
}

response:
{
    list: [
        {{SimpleFeed}},
        ...
    ], 
    next: 30  // 如果没有下一页，返回 0
}

```

4. 帖子详情

```
GET feed/{id}
response:
{
    forum: {{SimpleForum}},
    title: "标题",
    author: {
        name: "名字",
        cover: "http://full-url.jpg",
    },
    created_at: 14xxxxxxxx, //unix timestamp
    is_collected: 0, // 是否收藏
    is_thumbup: 0, // 是否点赞
    is_editable: 0, // 是否可编辑: 0 不可， 1 可以
    content: "html code" // 正文内容,
    thumbup_cnt: 123,
    thumbups: [
        {
            name: "用户1",
            cover: "image url"
        },
        ...
    ]
}

```

5. 帖子详情 (回复信息)

```
GET feed/{id}/reply
request:
{
    start: 0 // 分页
}

response:
{
    list: [
        {
            name: "用户1",
            cover: "image url",
            content: "string" // 回复内容,
            created_at: 14xxxxx, //unix timestamp
        },
        ...
    ],
    next: 30, // 分页
}

```

6. 发帖 

```
POST forum/{id}/feed
request:
{
    title: "xxx",
    content: "html",
}

```

7. 回复帖子

```
POST feed/{id}/reply

request:
{
    content: "string"
}
```


8. 收藏帖子
```
POST feed/{id}/collect 

request:
{
    type: 1 // 0 取消收藏，1 收藏
}

```

9. 点赞帖子

```
POST feed/{id}/thumbup

request:
{
    type: 1 // 0 取消点赞，1 点赞
}
```

10. 举报

```
POST report
requset:
{
    type: 1, // 1 - 帖子 , 2 - 评论
    id: 123,
}
```

11. 编辑帖子

```
PUT feed/{id}
request:
{
    title: "xxx",
    content: "html",
}
```
