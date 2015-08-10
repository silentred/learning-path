<?php

$client=new swoole_client(SWOOLE_SOCK_TCP, SWOOLE_SOCK_ASYNC);//TCP方式、同步
$client->on("receive", function($cli, $data = ""){
    //$data = $cli->recv(); //1.6.10+ 不需要
    if(empty($data)){
        $cli->close();
        echo "closed\n";
    } else {
        var_dump($data);
        //echo "received: $data\n";
        //sleep(1);
        //$cli->send("hello\n");
    }
    //var_dump($cli);
    $cli->close();
});

$client->on("close", function($cli){
    //$cli->close(); // 1.6.10+ 不需要
    echo "close\n";
});

$client->on("error", function($cli){
    exit("error\n");
});

$client->on("connect", function($cli) {
    echo "connected";
    $cli->send('show tables');//执行查询
});

$client->connect('127.0.0.1',9509);//连接
