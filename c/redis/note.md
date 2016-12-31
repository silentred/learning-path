# Redis 自问自答

## dict

1. Redis如何统计自己使用了多少内存？

void *zcalloc(size_t size) 要多分配一个 prefix_size， 这样在free 的时候就可以知道释放了多少内存,  有一个全局变量记录server的内存使用量。

2. dict *d = zmalloc(sizeof(*d)); 是什么用法？

sizeof(*d) 在编译期执行，根据前面定义的类型能够得知 `*d` 的类型和大小，和 
`zmalloc(sizeof(struct dict));` 是等价的。

3. 
