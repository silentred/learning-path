<?php

include "MySQL.php";

$config = array('host'=>'172.16.1.19', 'database'=>'1188test', 'user'=>'test', 'password'=>'test');
$client = new Swoole\Async\MySQL($config);

$start = microtime();
for($i=1 ; $i<5000; $i+=1){
    $result = $client->query("select * from video LIMIT {$i}, 10;", 
        function($mysqli, $result)use($i, $start){
        $result->fetch_all();
        if($i==4999){
            $end = microtime();
            echo "used time : ". ($end-$start);
        }
    });
}
/*
运行到这里脚本没有退出，不知道原因
 */




