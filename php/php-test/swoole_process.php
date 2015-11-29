<?php

$workers = [];
$worker_num = 3;//创建的进程数
$finished = false;
$lock = new swoole_lock(SWOOLE_MUTEX);

for($i=0;$i<$worker_num ; $i++){
    $process = new swoole_process('process');
    //$process->useQueue();
    $pid = $process->start();
    $workers[$pid] = $process;
}

foreach($workers as $pid => $process){
    //子进程也会包含此事件
    swoole_event_add($process->pipe, function ($pipe) use($process, $lock, &$finished) {
        $lock->lock();
        if(!$finished){
            $finished = true;
            $data = $process->read();
            echo "RECV: " . $data.PHP_EOL;
        }
        $lock->unlock();
    });
}

function process(swoole_process $process){
    $response = 'http response';
    $process->write($response);
    echo $process->pid,"\t",$process->callback .PHP_EOL;
}

for($i = 0; $i < $worker_num; $i++) {
    $ret = swoole_process::wait();
    $pid = $ret['pid'];
    echo "Worker Exit, PID=".$pid.PHP_EOL;
}
