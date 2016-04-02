<?php

$serv = new swoole_server("127.0.0.1", 9501);
$serv->set(array(
    'worker_num' => 2,
    'task_worker_num' => 2
));
function my_onStart($serv){
	echo "onStart\n";	
}
function my_onShutdown($serv){
	echo "onShutdown\n";
}
function my_onTimer($serv, $interval){
	echo "onTimer\n";
}
function my_onClose($serv, $fd, $from_id){
	echo "onClose\n";
}
function my_onWorkerStart($serv, $worker_id){
	echo "onWorkerStart\n";
}
function my_onFinish(swoole_server $serv, $task_id, $from_worker_id, $data){
	echo "onFinish\n";
}
function my_onWorkerStop($serv, $worker_id){
	echo "onStop\n";
}
function my_onConnect($serv, $fd, $from_id)
{
	echo "Client: fd=$fd is connect.\n";
}
function my_onReceive(swoole_server $serv, $fd, $from_id, $data){
	echo "Client: fd=$fd pid: " . posix_getpid() . " send: $data";
	$serv->task($fd . '|' . $data);
}
function my_onTask(swoole_server $serv, $task_id, $from_id, $data){
	list($fd, $recv) = explode('|', $data, 2);
	$serv->send(intval($fd), $recv);
	echo "Task: fd=$fd pid: " . posix_getpid() ." send: $recv";
}
function my_onWorkerError(swoole_server $serv, $worker_id, $worker_pid, $exit_code){
    echo "worker abnormal exit. WorkerId=$worker_id|Pid=$worker_pid|ExitCode=$exit_code\n";
}
$serv->on('Start', 'my_onStart');
$serv->on('Connect', 'my_onConnect');
$serv->on('Receive', 'my_onReceive');
$serv->on('Close', 'my_onClose');
$serv->on('Shutdown', 'my_onShutdown');
$serv->on('Timer', 'my_onTimer');
$serv->on('WorkerStart', 'my_onWorkerStart');
$serv->on('WorkerStop', 'my_onWorkerStop');
$serv->on('Task', 'my_onTask');
$serv->on('Finish', 'my_onFinish');
$serv->on('WorkerError', 'my_onWorkerError');
$serv->start();
