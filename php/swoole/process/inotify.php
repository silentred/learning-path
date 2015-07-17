<?php

$fd = inotify_init();

// modify表示写入内容，access表示读取内容，attribute表示meta信息修改（例如 user:group, 创建日期）
$watch_descriptor = inotify_add_watch($fd, __DIR__, IN_MODIFY|IN_ACCESS|IN_ATTRIB);

swoole_event_add($fd, function ($fd) {
    $events = inotify_read($fd);
    if ($events) {
        foreach ($events as $event) {
            echo "inotify Event :" . var_dump($event) . "\n";
        }
    }
});
