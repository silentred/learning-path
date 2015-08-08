<?php

$serv = stream_socket_server("tcp://0.0.0.0:8000", $errno, $errstr)
    or die ("cannot create server");

while(1){
    $conn = stream_socket_accept($serv);
    if(pcntl_fork() == 0){
        //child process
        $request = fread($conn);
        $response = "hello world";
        fwrite($conn, $response);
        fclose($conn);
        exit(0);
    }
}