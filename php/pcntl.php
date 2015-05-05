<?php
$childs = array();
// Fork some process.
for($i = 0; $i < 3; $i++) {
    declare(ticks=1);
    //设置信号处理器
    pcntl_signal(SIGCHLD, function ($signo){
        echo "\nchild process is ending... signal number is {$signo}\n";
        while (($pid = pcntl_waitpid(-1, $stat, WNOHANG) > 0) )
            echo "\n child terminated. {$pid}\n";
    });

    $pid = pcntl_fork();
    if($pid == -1)
        die('Could not fork');

    if ($pid) {
        //父进程得到子进程的pid号，一个大于0的值
        echo "this is parent, got child's pid: {$pid} \n";
        $childs[] = $pid;
        //在子进程结束之前结束，这时子进程会被init进程（pid=1）托管; 这就是孤儿进程
        //exit(0);
    } else {
        //子进程得到的$pid为0
        //取得父进程的pid
        $ppid = posix_getppid();
        $pid = posix_getpid();
        echo "this is child, number is {$i}. pid is {$pid} . my parent pid is {$ppid}. sleep 2 seconds\n";
        // Sleep $i+1 (s). The child process can get this parameters($i).
        sleep($i+2);
        //$ppid = posix_getppid();
        //echo "\n this is child, number is {$i} . my parent pid is {$ppid}. after sleep, end\n";
        
        // The child process needed to end the loop.
        exit();
    }
}

//等待子进程结束。子进程已经结束，父进程没有对其调用wait，导致子进程遗留的进程信息没有释放      
sleep(5);
//打印进程信息
echo system('ps -o pid,ppid,state,tty,command');
/*$handle = popen('ps -o pid,ppid,state,tty,command', 'r');
$content = stream_get_contents($handle);
pclose($handle);
echo $content . "\n";*/
//exit(0);
exit(0);

while(count($childs) > 0) {
    foreach($childs as $key => $pid) {
        $res = pcntl_waitpid($pid, $status, WNOHANG);
        
        // If the process has already exited
        if($res == -1 || $res > 0)
            unset($childs[$key]);
    }
    
    sleep(1);
}
echo "all child processes are released \n";

function signal_handler($signo){
    echo "child process is ending... signal number is {$signo}\n";
    while (($pid = pcntl_waitpid(-1, $stat, WNOHANG)) >0)
        sprintf("child %d terminated.\n", $pid);
}