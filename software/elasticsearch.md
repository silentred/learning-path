### 启动ES
`./elasticsearch -d`
`-d`表示daemon

###在索引中搜索
`curl -XGET 172.16.1.248:9200/default/_search?pretty&q=*`

### 测试analyze
`curl -XGET 172.16.1.248:9200/default/_analyze?analyzer=standard&pretty=true&text=杭州堆栈科技有限公司`

### 安装ICU插件后处理utf
`plugin -install elasticsearch/elasticsearch-analysis-icu/$VERSION`
$VERSION可以在 https://github.com/elastic/elasticsearch-analysis-icu 中查看。需要重启ES，在启动文字中可以看到加载到了analysis-icu。
可以用下面测试分词结果
`curl -XGET 172.16.1.248:9200/default/_analyze?tokenizer=icu_tokenizer&pretty=true&text=番茄鸡蛋`

[官方文档](https://www.elastic.co/guide/en/elasticsearch/guide/current/icu-plugin.html)

### 关闭ES
`curl -XPOST http://172.16.1.248:9200/_shutdown`