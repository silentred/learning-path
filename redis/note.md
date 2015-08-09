## Redis学习笔记

### DB
- 查看DB配置个数 `CONFIG GET databases`, 默认16个DB
- 查看各个DB存贮情况 `INFO keyspace`
- 切换DB `SELECT index`, index为0-15


### Key/Value

- 保存 `SET key "value"`。引号可以加或不加；若key存在则直接覆盖原值；value可以为string，int；完整命令为 `SET key value [EX seconds] [PX milliseconds] [NX|XX]`, `EX seconds`设置过期时长，seconds为int；`NX`表示only set the key if it does not exist; `XX`表示 only set the key if it already exits
- 读取 `GET key`
- 删除 `DEL key`, 返回删除的元素个数
- `SETNX key value` SET-if-not-exists. 仅当key不存在时才保存。返回影响个数。
- 自增 `INCR key`。当value为int时，自增1。
- 自增一定长度 `INCRBY key delta`, delta为int
- 过期 `EXPIRE key time` time为int，单位为秒。time秒后，key会被删除。
- 查看剩余生命时长 `TTL key`, time to live, 如果key过期被删除了，则返回-2，代表key不存在。如果key没有设置过期时长，则ttl结果为-1。
- 是否存在key `EXISTS key`
- `EXPIREAT key timestamp` 在某个时间点过期，如果timestamp小于当前Unix timestamp，则立即删除
- `KEYS pattern` 数据库较大时有性能问题，建议生产环境不用。
- `PERSIST key` 清除过期，返回0或1
- `PEXPIRE key milliseconds` 毫秒过期
- `RENAME key newkey`
- `SORT key [BY pattern] [LIMIT offset count] [GET pattern [GET pattern ...]] [ASC|DESC] [ALPHA] [STORE destination]` , 连表排序`SORT mylist BY weight_*`, `SORT mylist BY weight_* GET object_* GET #`,
`#`表示get the element itself. 连Hash表`SORT mylist BY weight_*->fieldname GET object_*->fieldname`




### List队列

- 元素加入尾部 `RPUSH key value`， 返回插入后list的总长度
- 加入头部 `LPUSH key value`
- 取部分队列元素 `LRANGE key index index2` index为int，index2为-1表示最后一个元素。index，index2两个元素都包含在结果集中。例如 `LRANGE key 0 1`结果中有两个元素。
- 长度 `LLEN key`
- 从左侧删除 `LPOP key`, 返回删除的元素
- 从右删除 `RPOP key`

### Set集合

- 添加元素 `SADD key value`, 返回添加的元素的个数
- 删除元素 `SREM key value`， 返回删除的元素个数
- 检测set是否已经存在value `SISMEMBER key value`, 返回0或1；一个只能检测一个value。
- 列出所有元素 `SMEMBERS key`
- 多集合并集 `SUNION key1 key2`，返回并集的结果集


### Sorted Set有序集合

- 添加元素 `ZADD key point value`, point 为分数int。
- 取集合部分元素 `ZRANGE key index1 index2`, 按point从小到大排列

### Hashes 哈希

- 添加元素字段 `HSET key field value`, 例如 `HSET user:10 name "Jason W."`。field是string。
- 设置多个字段和值 `HMSET key field1 value1 field2 value2`, M代表multiple
- 列出元素所有字段 `HGETALL key`
- 列出某个字段 `HGET key field` 
- 递增 `HINCRBY key field delta`, delta 为递增的数值int。如果field不存在，则创建filed，值为delta。返回该字段递增后的结果，int。
- 删除字段 `HDEL key field`， 可以删除多个字段; 如果删除整个hash，用`DEL key`
- 判断字段是否存在 `HEXISTS key field`




