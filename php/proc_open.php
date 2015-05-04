<?php
    // make gz file
    $fd=fopen("/tmp/testPipe", "w");
    for($i=0;$i<100000;$i++)
        fwrite($fd, md5($i)."\n");
    fclose($fd);

    if(is_file("/tmp/testPipe.gz"))
        unlink("/tmp/testPipe.gz");
    system("gzip /tmp/testPipe");

    // open process
    $pipesDescr=array(
        0 => array("pipe", "r"),
        1 => array("pipe", "w"),
        2 => array("file", "/tmp/testPipe.log", "a"),
    );

    $process=proc_open("zcat", $pipesDescr, $pipes);
    if(!is_resource($process)) throw new Exception("popen error");

    // set both pipes non-blocking
    stream_set_blocking($pipes[0], 0);
    stream_set_blocking($pipes[1], 0);
    //这里如果不用 non-blocking，会产生死锁

    // read the file /tmp/testPipe.gz
    /*$text="";
    $fd=fopen("/tmp/testPipe.gz", "r");
    while (!feof($fd)) {
        $text .= fread($fd, 16384*4);
    }
    fclose($fd);
    echo $text;
    die(0);
    得到的是压缩过的文字，乱码, 结果和 cat /tmp/testPipe.gz一样
    cat /tmp/testPipe.gz | zcat 可以得到正常的文字
    */

    $text="";
    $fd=fopen("/tmp/testPipe.gz", "r");
    while(!feof($fd))
    {
        $str=fread($fd, 16384*4);
        $try=3;
        while($str)
        {
            $len=fwrite($pipes[0], $str); //一次不一定全部写入，可能需要分多次写入
            while($s=fread($pipes[1], 16384*4))
                $text.=$s;

            if(!$len)
            {
                // if yo remove this paused retries, process may fail
                usleep(200000);
                $try--;
                if(!$try)
                    throw new Exception("fwrite error");
            }
            $str=substr($str, $len);//如果一次没有写完，则继续循环
        }
        echo strlen($text)."\n";
    }
    fclose($fd);
    fclose($pipes[0]);

    // reading the rest of output stream
    stream_set_blocking($pipes[1], 1);
    while(!feof($pipes[1]))
    {
        $s=fread($pipes[1], 16384);
        $text.=$s;
    }

    echo strlen($text)." / 3 300 000\n";