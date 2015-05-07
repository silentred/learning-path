#Elasicsearch

##start service

	bin/elasticsearch -d
默认会启动一个随机命名的master节点，-d代表daemon

## Node status
### Node health
	curl 'localhost:9200/_cat/health?v'
查看节点状态

### Node list
	curl 'localhost:9200/_cat/nodes?v'
查看节点列表

## Index
### Index list
	curl 'localhost:9200/_cat/indices?v'
索引节点列表

### Create Index
	curl -XPUT 'localhost:9200/customer?pretty'
创建名为customer的索引

### add ducument
	curl -XPUT 'localhost:9200/customer/external/1?pretty' -d '{"name": "John Doe"}'
添加文档
### get document
	curl -XGET 'localhost:9200/customer/external/1?pretty'
查看刚才添加的文档
### delete an index
	curl -XDELETE 'localhost:9200/customer?pretty'
删除索引

###RESTful API的模式：
	curl -X<REST Verb> <Node>:<Port>/<Index>/<Type>/<ID>
记住这个比较好

