<?php


function read_cb($socket, $flag, $base) {
    fread($socket);
    fwrite($socket, "hello world");
}

function accept_cb($socket, $flag, $base) {
    $conn = stream_socket_accept($socket, 0);
    stream_set_blocking($conn, 0);
    $event = event_new();
    event_set($event, $conn, EV_READ | EV_PERSIST, read_cb, $base);
    event_base_set($event, $base);
    event_add($event);
}

$serv = stream_socket_server("tcp://0.0.0.0:8000", $errno, $errstr)
    or die ("cannot create server");

// 创建固定数量个子进程，循环串行利用
for ($i=0; $i < 8; $i++) { 
    if(pcntl_fork() == 0){
        $base = event_base_new();
        $event = event_new();
        event_set($event, $socket, EV_READ | EV_PERSIST, accept_cb, $base);
        event_base_set($event, $base);
        event_add($event);
        event_base_loop($base);
        exit(0);
    }
}
