## Redis学习笔记

### Key/Value

- 保存 `SET key "value"`。引号可以加或不加；若key存在则直接覆盖原值；value可以为string，int；
- 读取 `GET key`
- 删除 `DEL key`, 返回删除的元素个数
- `SETNX key value` SET-if-not-exists. 仅当key不存在时才保存。返回影响个数。
- 自增 `INCR key`。当value为int时，自增1。
