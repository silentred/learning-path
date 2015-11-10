# Sleep 会被 Signal打断

无论是在 signal handler 中还是在外部的sleep($second)都会被打断，并且返回剩余的秒数（linux平台下）。
windows平台下返回一个常数。
所以如果想测试pcntl_signal(), 切记要在子进程中用while循环sleep， 不然sleep被打断，直接退出， 导致看起来像是在handler之后紧跟着执行了默认信号处理器，比较难找到问题所在。


# 关于 sql 注入

addslashes($sql) 可以对mysql关键词, 这些字符是单引号（'）、双引号（"）、反斜线（\）与 NUL（NULL 字符）
如果数据来自 $_COOKIE, $_GET, $POST, 使用前用 get_magic_quotes_gpc() 判断有没有开启 magic_quotes_gpc 配置, 防止重复转义。 

