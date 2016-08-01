Feed相关接口
目录
1.Feed发布接口
2.Feed列表(关注)
3.Feed列表(最新)
4.Feed列表(附近)
5.Feed抢赞
6.删除Feed

1.Feed发布接口
POST /v1/feeds
{
    type: int, //必填 1:图文 2:视频 3:直播
    cover: string, // 必填
    text: string, // 选填
    video: jsonString // type=2时必填
    pictures: jsonString // type=1时必填
    long: float // 选填
    lat: float // 选填
    poi: jsonString // 选填
}
成功返回:
{id: int}
出错:
{error_code: 202500} // 保存Feed失败


2.获取Feed列表(关注)
GET /v1/feeds/subcsribe
{
    start: string, // 选填
    limit: int, // 选填 default 10,
    long: float, // 选填
    lat: float, // 选填
}
成功返回
{
    list: [
        AllFeedObject, AllFeedObject, ..., AllFeedObject
    ],
    next: string
}
出错返回:
{error_code: 202404} // 找不到Feed


3.获取Feed列表(最新)
GET /v1/feeds/newest
参数与返回值同关注

4.获取Feed列表(附近)
GET /v1/feeds/nearby
参数与返回值同关注

5.feed抢赞
POST /v1/feeds/game
{
    object_id: int,
    object_type: int, // 1:服务 2:相册 3:故事 4:Feed 5:直播
    index: int, 位置0-4
}
返回值
成功返回:
{result: 'ok'}
失败返回:
{error_code: 202500} // 抢赞失败

6.删除Feed
POST /v1/feeds/{id}/delete
成功返回:
{result: 'ok'}
失败返回:
{error_code: 202500} // 抢赞失败
Feed接口相关的模型:
包含所有Feed类型的模型
AllFeedObject:{
    object_type: int, // 1:服务 2:相册 3:故事 4:Feed 5:直播
    object_id: int,
    object: FeedObject or ServiceObject, //根据object_type不同而不同
}

除开服务的Feed模型
FeedObject:{
    id: int,
    user: {
        uid: int,
        fullname: string,
        avatar: string,
        sex: int,
        truthful: int,
        age: int,
        intro: string
    },
    text: string,
    type: int, // 1:图片 2:视频 3:直播
    pictures: [
        {
            url: string,
            w: int,
            h: int
        },{
            url: string,
            w: int,
            h: int
        }
    ],
    video: {
        url: string,
        w: int,
        h: int
    },
    stream_id: string,
    distance: int,
    poi: {
        long: float,
        lat: float,
        name: string,
        city: string
    },
    praise: int, //点赞数
    praise_fastest: { // 点赞最快
        uid: int,
        fullname: string,
        avatar: string,
        sex: int,
        truthful: int,
        age: int,
        intro: string
    },
    praise_most: { // 点赞最多
        uid: int,
        fullname: string,
        avatar: string,
        sex: int,
        truthful: int,
        age: int,
        intro: string
    },
    praise_games: [ // 抢赞用户
        {
            uid: int,
            fullname: string,
            avatar: string,
            sex: int,
            truthful: int,
            age: int,
            intro: string,
            index: int, // 0-4
        },
        {
            uid: int,
            fullname: string,
            avatar: string,
            sex: int,
            truthful: int,
            age: int,
            intro: string,
            index: int, // 0-4
        }
    ],
    share: int, //分享数
    share_url: string,
    is_collect: int,
    collect_count: int
}


服务的模型
ServiceObject:{
    id: int,
    user: {
        uid: int,
        fullname: string,
        avatar: string,
        sex: int,
        truthful: int,
        age: int,
        intro: string
    },
    title: string,
    raw_title: string,
    cover: string,
    is_free: string,
    price: float,
    country: string,
    province: string,
    city: string,
    type: int, // 1玩法 2 技能 3美食
    service_way: int,//服务方式 1一对一 2一对多
    scene: int, // 1:来我这 2:去你那
    equipment: int, // 1:我提供 2:自己拿
    restaurant: string, // 餐厅
    arbitrary: int, 是否预约
    distance: int,
    poi: {
        long: float,
        lat: float,
        name: string,
        city: string
    },
    praise: int, //点赞数
    praise_fastest: { // 点赞最快
        uid: int,
        fullname: string,
        avatar: string,
        sex: int,
        truthful: int,
        age: int,
        intro: string
    },
    praise_most: { // 点赞最多
        uid: int,
        fullname: string,
        avatar: string,
        sex: int,
        truthful: int,
        age: int,
        intro: string
    },
    praise_games: [ // 抢赞用户
        {
            uid: int,
            fullname: string,
            avatar: string,
            sex: int,
            truthful: int,
            age: int,
            intro: string,
            index: int, // 0-4
        },
        {
            uid: int,
            fullname: string,
            avatar: string,
            sex: int,
            truthful: int,
            age: int,
            intro: string,
            index: int, // 0-4
        }
    ],
    share: int, //分享数
    share_url: string,
    is_collect: int,
    collect_count: int
}