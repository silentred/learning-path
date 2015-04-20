<?php

$server = new swoole_websocket_server("", 9501);

$server->on('open', function (swoole_websocket_server $server, $request) {
    echo "server: handshake success with fd{$request->fd}\n";
});

$server->on('message', function (swoole_websocket_server $server, $frame) {
    echo "receive from {$frame->fd}:{$frame->data},opcode:{$frame->opcode},fin:{$frame->finish}\n";
    
    $conn_list = $server->connection_list();
    //var_dump($conn_list); 广播
    foreach($conn_list as $fd){
        $server->push($fd, "from: client{$frame->fd}, content: ".$frame->data);
    }
    //$server->push($frame->fd, "from: client{$fd}, content: ".$frame->data);
    
});

$server->on('close', function ($ser, $fd) {
    echo "client {$fd} closed\n";
});

$server->start();
