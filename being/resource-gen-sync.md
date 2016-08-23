# 资源生成和同步

## 资源的需求

- 消息视频 需要生成 第一秒截图，截图的模糊图，第一秒开始的webp(长2秒)
- 消息图片 需要生成 缩略模糊图
- 头像 需要生成 缩略图
- 背景 无需新资源

这些资源的原始资源+新生成资源 都需要同步到 qiniu 和 s3，双向的同步，传到qiniu的同步到s3，传到s3的同步到qiniu。


## 目前方案的缺点

- 两重回调，qiniu生成资源结果一个回调，同步s3的结果一个回调
- 业务表需要额外的字段保存 是否有新生成的资源， 是否同步到了s3
- 依赖qiniu的API生成新的资源，如果换成原始资源先上传s3则会带来新的工作量
- 和业务服务混在一起，占用资源

## 解决方案

用一个服务管理这些资源的生成和同步。

- 无回调：自己解决生成资源的问题，不依赖qiniu，同步上传新资源，少一次回调；接着同步上传s3, 少一次回调；
- 记录结果：新资源和生成结果，同步结果，原始资源的同步结果，都在此服务内保存，提供接口查询。

输入新资源：异步接口，返回job_id;

```
POST /resource/new

request:
{
   fromBucket: "fame-public",
   key: "xxx",
   type: "msg_video",
   toBucket: "fame-s3"
}
```

查询可用URL:

```
GET /resource/url

query:
{
    key: "xxx",
    prefer_storage: s3 | qiniu
}

response:
{
    url: xxx,
    cover_url: xxx,
    webp_url: xxx,
    blur_url: xxx
}
```

工作量大约一周，希望各位给出意见，该方案是否可行
