# ELK Stack 日志收集

## 数据收集：

- 收集原始数据
- 格式化数据，不同的应用log原始格式一般不相同，这里要么统一原始log格式，要么针对每一种log格式配置不一样的 config 文件, 来格式化
- 输出数据到不同的位置

### (Filebeat + Logstash) vs Flume

Logstash的插件种类较多，两者都支持输出到 hdfs, elasticsearch，kafka; 
都支持 fanout: 同一份数据复制到不同的目的地，例如 存储到hdfs, 存储到 es 索引，push 到 kafka 做统计

这两者用哪个都可以，建议暂时使用 logstash, 插件比较全，资料比较多。目前可能不需要 hdfs，只存储到 ES 就够用了。

1. Filebeat (收集) => Logstash (数据处理) => elasticsearch（存储+索引）=> Kibana (报表，检索 web界面)
2. Flume(collector 收集 + sink 数据处理) => Hadoop, HBase, elasticsearch

## 告警
ES 自带的 watcher 插件可以完成，目前看来是比较紧急的需求。

## 数据展示
Kibana + ES, Kibana 支持 lucene 搜索语法，支持自定义图表。目前来看主要的需求只是在搜索。

## Log格式
目前的 web log 没有很好的格式化，可以考虑加上一些公共字段，例如 请求时间，uid, request_id 等. 

