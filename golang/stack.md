扩容函数:
runtime.morestack

查看内存分配:
curl -s http://localhost:port/debug/pprof/heap?debug=1 | grep -A 20 runtime.MemStats

扩容策略:
go在1.3之前栈扩容采用的是分段栈（Segemented Stack），在栈空间不够的时候新申请一个栈空间用于被调用函数的执行， 执行后销毁新申请的栈空间并回到老的栈空间继续执行，当函数出现频繁调用（递归）时可能会引发hot split。为了避免hot split, 1.3之后采用的是连续栈（Contiguous Stack），栈空间不足的时候申请一个2倍于当前大小的新栈，并把所有数据拷贝到新栈， 接下来的所有调用执行都发生在新栈上。

缩容:
栈收缩不是在函数调用时发生的，是由垃圾回收器在垃圾回收时主动触发的。基本过程是计算当前使用的空间，小于栈空间的1/4的话， 执行栈的收缩，将栈收缩为现在的1/2，否则直接返回。

栈缩容的目标是提高内存利用率，但在缩容过程中会存在栈拷贝和写屏障(write barrier)，对于一些准实时应用可能会存在一些影响。 好在go提供了可设置的参数，需要的话大家可以通过设置环境变量 GODEBUG=gcshrinkstackoff=1 来关闭栈缩容。关闭栈缩容后， 需要承担栈持续增长的风险，在关闭前需要慎重考虑。

http://studygolang.com/articles/10597