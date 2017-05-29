mysql 5.7
144cpu 512G 160w QPS (OLTP read)

动态 bufferpool

redo log <= 512G

innodb_file_per_table 默认 on, 独立表空间, 可以使用 transportable tablespaces

query cache, 建议关闭

独立 undo 表空间

max_execution_time sql超时中断, ms, 针对select

innodb_numa_interleave ? numa? 导致 swap? 

replication filter

并行复制? 组提交?

NVMe ?

PTR exchange ? 
gost from github ?