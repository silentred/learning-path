# PHP编程中的锁

> 最近看了《理解Linux进程》这本开源书，[链接](http://www.linuxprocess.com/)。该书描述了linux中的进程概念，对锁和进程间通信(IPC)有一些总结。不过该书的描述语言是golang, 平时用的比较少，就想对应概念找找php中的接口。

## 文件锁
全名叫 `advisory file lock`, 书中有[提及](http://www.linuxprocess.com/process_advanced/file_lock.html)。 这类锁比较常见，例如 mysql, php-fpm 启动之后都会有一个pid文件记录了进程id，这个文件就是文件锁。

这个锁可以防止重复运行一个进程，例如在使用crontab时，限定每一分钟执行一个任务，但这个进程运行时间可能超过一分钟，如果不用进程锁解决冲突的话两个进程一起执行就会有问题。

使用PID文件锁还有一个好处，方便进程向自己发停止或者重启信号。例如重启php-fpm的命令为 
```
kill -USR2 `cat /usr/local/php/var/run/php-fpm.pid`
```
发送`USR2`信号给pid文件记录的进程，信号属于进程通信，会另开一个篇幅。

php的接口为`flock`，文档比较详细。先看一下定义，`bool flock ( resource $handle , int $operation [, int &$wouldblock ] )`. 

- `$handle`是文件系统指针，是典型地由 fopen() 创建的 resource(资源)。这就意味着使用flock必须打开一个文件。
- `$operation` 是操作类型。
- `&$wouldblock` 如果锁是阻塞的，那么这个变量会设为1.

需要注意的是，这个函数默认是阻塞的，如果想非阻塞可以在 operation 加一个 bitmask `LOCK_NB`. 接下来测试一下。

```
$pid_file = "/tmp/process.pid";
$pid = posix_getpid();
$fp = fopen($pid_file, 'w+');
if(flock($fp, LOCK_EX | LOCK_NB)){
	echo "got the lock \n";
	ftruncate($fp, 0);      // truncate file
    fwrite($fp, $pid);
    fflush($fp);            // flush output before releasing the lock
    sleep(300); // long running process
    flock($fp, LOCK_UN);    // 释放锁定
} else {
	echo "Cannot get pid lock. The process is already up \n";
}
fclose($fp);
```
保存为 `process.php`，运行`php process.php &`, 此时再次运行`php process.php`，就可以看到错误提示。flock也有共享锁，`LOCK_SH`.

## 互斥锁和读写锁

### sync模块中的Mutex

Mutex是一个组合词，mutual exclusion。用pecl安装一下sync模块, `pecl install sync`。 文档中的SyncMutex只有两个方法，lock 和 unlock， 我们就直接上代码测试吧。没有用IDE写，所以cs异常丑陋，请无视。

```
$mutex = new SyncMutex("UniqueName");

for($i=0; $i<2; $i++){
	$pid = pcntl_fork();
	if($pid <0){
		die("fork failed");
	}elseif ($pid>0){
		echo "parent process \n";
	}else{
		echo "child process {$i} is born. \n";
		obtainLock($mutex, $i);
	}
}

while (pcntl_waitpid(0, $status) != -1) { 
	$status = pcntl_wexitstatus($status); 
	echo "Child $status completed\n"; 
}

function obtainLock ($mutex, $i){
	echo "process {$i} is getting the mutex \n";
	$res = $mutex->lock(200);
	sleep(1);
	if (!$res){
		echo "process {$i} unable to lock mutex. \n";
	}else{
		echo "process {$i} successfully got the mutex \n";
		$mutex->unlock();
	}
	exit();
}

```
保存为`mutex.php`, run `php mutex.php`, output is 
```
parent process 
parent process 
child process 1 is born. 
process 1 is getting the mutex 
child process 0 is born. 
process 0 is getting the mutex 
process 1 successfully got the mutex 
Child 0 completed
process 0 unable to lock mutex. 
Child 0 completed
```
这里子进程0和1不一定谁在前面。但是总有一个得不到锁。这里`SyncMutex::lock(int $millisecond)`的参数是 millisecond, 代表阻塞的时长， -1 为无限阻塞。

### sync模块中的读写锁

`SyncReaderWriter`的方法类似，`readlock`, `readunlock`, `writelock`, `writeunlock`,成对出现即可，没有写测试代码，应该和Mutex的代码一致，把锁替换一下就可以。

### sync模块中的Event

感觉和golang中的`Cond`比较像，`wait()`阻塞，`fire()`唤醒Event阻塞的一个进程。有一篇[好文](http://openmymind.net/Condition-Variables/)介绍了`Cond`, 可以看出`Cond`就是锁的一种固定用法。`SyncEvent`也一样。
php文档中的例子显示，fire()方法貌似可以用在web应用中。

上测试代码

```
for($i=0; $i<3; $i++){
	$pid = pcntl_fork();
	if($pid <0){
		die("fork failed");
	}elseif ($pid>0){
		//echo "parent process \n";
	}else{
		echo "child process {$i} is born. \n";
		switch ($i) {
		case 0:
			wait();
			break;
		case 1:
			wait();
			break;
		case 2:
			sleep(1);
			fire();
			break;
		}
	}
}

while (pcntl_waitpid(0, $status) != -1) { 
	$status = pcntl_wexitstatus($status); 
	echo "Child $status completed\n"; 
}

function wait(){
	$event = new SyncEvent("UniqueName");
	echo "before waiting. \n";
	$event->wait();
	echo "after waiting. \n";
	exit();
}

function fire(){
	$event = new SyncEvent("UniqueName");
	$event->fire();
	exit();
}
```
这里故意少写一个fire(), 所以程序会阻塞，证明了 fire() 一次只唤醒一个进程。

### pthreads模块
貌似也看到了Mutex, Cond, Pool. 没来得及看，看完再补充。 

## 信号量

### sync模块中的信号量

`SyncSemaphore`文档中显示，它和Mutex的不同之处，在于Semaphore一次可以被多个进程(或线程)得到，而Mutex一次只能被一个得到。所以在`SyncSemaphore`的构造函数中，有一个参数指定信号量可以被多少进程得到。
`public SyncSemaphore::__construct ([ string $name [, integer $initialval [, bool $autounlock ]]] )` 就是这个`$initialval` (initial value)

```
$lock = new SyncSemaphore("UniqueName", 2);

for($i=0; $i<2; $i++){
	$pid = pcntl_fork();
	if($pid <0){
		die("fork failed");
	}elseif ($pid>0){
		echo "parent process \n";
	}else{
		echo "child process {$i} is born. \n";
		obtainLock($lock, $i);
	}
}

while (pcntl_waitpid(0, $status) != -1) { 
	$status = pcntl_wexitstatus($status); 
	echo "Child $status completed\n"; 
}

function obtainLock ($lock, $i){
	echo "process {$i} is getting the lock \n";
	$res = $lock->lock(200);
	sleep(1);
	if (!$res){
		echo "process {$i} unable to lock lock. \n";
	}else{
		echo "process {$i} successfully got the lock \n";
		$lock->unlock();
	}
	exit();
}
```
这时候两个进程都能得到锁。

### sysvsem模块中的信号量

- `sem_get` 创建信号量
- `sem_remove` 删除信号量（一般不用）
- `sem_acquire` 请求得到信号量
- `sem_release` 释放信号量。和 `sem_acquire` 成对使用。

```
$key = ftok('/tmp', 'c');
$sem = sem_get($key);

for($i=0; $i<2; $i++){
	$pid = pcntl_fork();
	if($pid <0){
		die("fork failed");
	}elseif ($pid>0){
		//echo "parent process \n";
	}else{
		echo "child process {$i} is born. \n";
		obtainLock($sem, $i);
	}
}

while (pcntl_waitpid(0, $status) != -1) { 
	$status = pcntl_wexitstatus($status); 
	echo "Child $status completed\n"; 
}
sem_remove($sem); // finally remove the sem

function obtainLock ($sem, $i){
	echo "process {$i} is getting the sem \n";
	$res = sem_acquire($sem, true);
	sleep(1);
	if (!$res){
		echo "process {$i} unable to get sem. \n";
	}else{
		echo "process {$i} successfully got the sem \n";
		sem_release($sem);
	}
	exit();
}
```
这里有一个问题，`sem_acquire()`第二个参数$nowait默认为false，阻塞。我设为了true，如果得到锁失败，那么后面的`sem_release`会报警告 `PHP Warning:  sem_release(): SysV semaphore 4 (key 0x63000081) is not currently acquired in /home/jason/sysvsem.php on line 33`, 所以这里的release操作必须放在得到锁的情况下执行，前面的几个例子中没有这个问题，没得到锁执行release也不会报错。当然最好还是成对出现，确保得到锁的情况下再release。 

此外，`ftok`这个方法的参数有必要说明下，第一个 必须是existing, accessable的文件, 一般使用项目中的文件，第二个是单字符字符串。返回一个int。

输出为

```
parent process 
parent process 
child process 1 is born. 
process 1 is getting the mutex 
child process 0 is born. 
process 0 is getting the mutex 
process 1 successfully got the mutex 
Child 0 completed
process 0 unable to lock mutex. 
Child 0 completed
```

> 最后，如果文中有错误的地方，希望大神指出，帮助一下菜鸟进步，谢谢各位。
