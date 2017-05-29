<?php

$filePath = '/tmp/comics.txt';
$fd = fopen($filePath, 'a+');

for ($i=1000; $i < 5000; $i++) { 
    $url = sprintf("http://v2.api.dmzj.com/comic/%d.json", $i);
    $data = httpGet($url);
    $obj = json_decode($data, true);
    if ($obj) {
        $title = $obj['title'];
        $id = $obj['id'];
        fwrite($fd, "$id - $title \n");
    }
}

fclose($fd);

function httpGet($url) {
	$ch = curl_init();
	$timeout = 5;
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, $timeout);
	$data = curl_exec($ch);
	curl_close($ch);
	return $data;
}

