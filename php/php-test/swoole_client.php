<?php

$client = new swoole_client(SWOOLE_SOCK_TCP, SWOOLE_SOCK_ASYNC);
//设置事件回调函数
$client->on("connect", function($cli) {
    $req = "GET / HTTP/1.1\r\n
    Host: www.baidu.com\r\n
    Connection: keep-alive\r\n
    Cache-Control: no-cache\r\n
    Pragma: no-cache\r\n\r\n";

    for ($i=0; $i < 3; $i++) {
        $cli->send($req);
    }
});
$client->on("receive", function($cli, $data){
    echo "Received: ".$data."\n";
    exit(0);
    $cli->sleep(); // swoole >= 1.7.21
});
$client->on("error", function($cli){
    echo "Connect failed\n";
});
$client->on("close", function($cli){
    echo "Connection close\n";
});
//发起网络连接
$client->connect('183.207.95.145', 80, 1);
