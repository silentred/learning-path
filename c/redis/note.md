# Redis Q&A

## dict

1. void *zcalloc(size_t size) 为什么要多分配一个 prefix_size ?
在free的时候需要知道释放了多少内存, 有一个全局变量记录server的内存使用量

2. dict *d = zmalloc(sizeof(*d)); 是什么用法？
sizeof(*d) 在编译期执行，根据前面定义的类型能够得知 `*d` 的类型和大小

3. 
