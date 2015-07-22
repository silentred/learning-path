<?php
$jobs = [];
$process = new swoole_process('callback_function', true);
//var_dump($process);
$process->job = "it is a job";
$pid = $process->start();

//var_dump($process); // process对象
// class swoole_process#1 (3) {
//   public $pipe =>
//   int(4)
//   public $callback =>
//   string(17) "callback_function"
//   public $pid =>
//   int(10389)
// }
//var_dump($pid);

function callback_function(swoole_process $worker)
{
	var_dump($worker->job);
    sleep(1);
    //$worker->exec('/usr/local/bin/php', array(__DIR__.'/swoole_server.php'));
    //$worker->write("hello\n");
    //var_dump($worker);
    //$worker->exit(0);

    //接受主进程的消息，并回复一个"hello master"
	/**
    swoole_event_add($worker->pipe, function($pipe) {
        $worker = $GLOBALS['process'];
        $recv = $worker->read();
        //这里var_dump不是指向标准输出，而是指向 $worker->pipe, 发出的数据在主进程的$process->read()中可以接收到
		// 这个特性在构造函数的第二个参数，修改为false即可打印到stdout
        var_dump("From Master: $recv");
        sleep(2);
        //send data to master
        $worker->write("hello master\n");
        sleep(2);
        $worker->exit(0);
    });
	**/
}

//发送给子进程$process一个消息
//$process->write("Hi, I am writing into a worker");
// 同步阻塞，可以用swoole_event_add加入事件监听
var_dump($process->read());

// swoole_event_add($process->pipe, function($pipe){
//     $worker = $GLOBALS['process'];
//     $recv = $worker->read();
//     //var_dump($recv);
//     echo "I am from eventloop. Content: $recv \n";
// });

echo "I must come first \n";
swoole_process::wait();
