<?php

$fd = fopen(__FILE__, 'a');
$len = fwrite($fd, "\n");
fclose($fd);

chdir(__DIR__.'/../');
exec("git add *");
$today = date("Y-m-d");
exec("git commit -m \"{$today}\" ");
exec("git push");









