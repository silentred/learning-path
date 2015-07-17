<?php

$workers = [];
$worker_num = 2;

for($i = 0; $i < $worker_num; $i++)
{
    $process = new swoole_process('callback_function', false, false);
    $process->useQueue();
    $pid = $process->start();
    //$process->daemon(true);
    $workers[$pid] = $process;
    //echo "Master: new worker, PID=".$pid."\n";
}

function callback_function(swoole_process $worker)
{
    //echo "Worker: start. PID=".$worker->pid."\n";
    //recv data from master
    $cnt = 0;
    while ($cnt<2) {
        // 如果队列里没有数据，则pop方法阻塞等待
        $recv = $worker->pop();
        echo "From Master: $recv\n";
        $cnt++;
    }
    sleep(1);
    $worker->exit(0);
}

foreach($workers as $pid => $process)
{
    $process->push("hello worker[$pid]\n");
}

foreach($workers as $pid => $process)
{
    $process->push("hello2 worker[$pid]\n");
    //sleep(1);
}


for($i = 0; $i < $worker_num; $i++)
{
    $ret = swoole_process::wait();
    $pid = $ret['pid'];
    unset($workers[$pid]);
    echo "Worker Exit, PID=".$pid.PHP_EOL;
}
