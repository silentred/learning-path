# PHPSpider

## 想法
模仿 pyspider 写一个爬虫。用 `swoole_event_add` 实现fetch url的异步操作。
队列实现异步操作。

## 结构
jobGenerator: 生成job，推入队列
scheduler: 确定是否应该去抓这个页面
fetcher: 从队列中去取需要抓取的任务
resultHandler: 处理从fetcher返回的结果




