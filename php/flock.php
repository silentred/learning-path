<?php
for($i = 0; $i < 1; $i ++)
{
    $db = new mysqli("192.168.2.50", "test", "test", "test");
    $lock = fopen("/tmp/mysql_lock.txt", 'w+');
    if ($db->connect_errno) 
    {
        printf("Connect failed: %s\n", $db->connect_error);
        exit();
    }
}

for($i = 0; $i < 5; $i++)
{
    if(pcntl_fork() > 0)
    {
        continue;
    }
    if (flock($lock, LOCK_EX))
    {
        $result = $db->query('show tables');
    }
    flock($lock, LOCK_UN); 
    
    if (empty($result)) 
    {
            print('Invalid query: ' . $db->error."\n");
    }
    else
    {
        while ($row = $result->fetch_assoc()) 
        {
            echo "#".posix_getpid(),"\t";
            var_dump($row);
            echo "\n";
        }
        $result->close();
    }
    sleep(1000);
    exit;
}
sleep(1000);