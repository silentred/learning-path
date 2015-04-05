<?php
$client = new Yar_Client("http://localhost/server.php");
/* the following setopt is optinal */
$client->SetOpt(YAR_OPT_CONNECT_TIMEOUT, 1);

/* call remote service */
$result = $client->some_method("parameter");
print_r($result. '<br>');


//Concurrent call
function callback($retval, $callinfo) {
     print_r($retval . ' / callback / ');
     var_dump($callinfo);
     print_r('<br>'); 
}

function error_callback($type, $error, $callinfo) {
	var_dump($type);
	var_dump($error);
	var_dump($callinfo);
    error_log($error);
}

Yar_Concurrent_Client::call("http://localhost/server.php", "some_method", array("Concurrent 1"), "callback");
// if the callback is not specificed, callback in loop will be used
Yar_Concurrent_Client::call("http://localhost/server.php", "some_method", array("Concurrent 2"));
//this server accept json packager
Yar_Concurrent_Client::call("http://localhost/server.php", "some_method", array("Concurrent 3"), "callback", "error_callback", array(YAR_OPT_PACKAGER => "json"));
//custom timeout 
Yar_Concurrent_Client::call("http://localhost/server.php", "some_method", array("Concurrent 4"), "callback", "error_callback", array(YAR_OPT_TIMEOUT=>1));

//send the requests, 
//the error_callback is optional
Yar_Concurrent_Client::loop("callback", "error_callback"); 

?>