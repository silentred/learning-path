<?php

$filePath = '/tmp/comics.txt';
$fd = fopen($filePath, 'a+');

for ($i=15000; $i < 20000; $i++) { 
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

function httpPost($url, $fields){
	//url-ify the data for the POST
	foreach($fields as $key=>$value) { $fields_string .= $key.'='.$value.'&'; }
	rtrim($fields_string, '&');
	//open connection
	$ch = curl_init();
	curl_setopt($ch,CURLOPT_URL, $url);
	curl_setopt($ch,CURLOPT_POST, count($fields));
	curl_setopt($ch,CURLOPT_POSTFIELDS, $fields_string);
	$result = curl_exec($ch);
	curl_close($ch);
}

function sub($uid, $comicID){
	$url = 'http://v2.api.dmzj.com/subscribe/add';
	//channel=ios&obj_ids=12090&type=mh&uid=102198270&version=2.2.4
	$fields = [
		'channel' => 'ios',
		'obj_ids' => $comicID,
		'type' => 'mh',
		'uid' => $uid,
		'version' => '2.2.4',
	];

	httpPost($url, $fields);
}