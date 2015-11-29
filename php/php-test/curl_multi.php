<?php

// build the individual requests as above, but do not execute them
 $ch_1 = curl_init('http://www.baidu.com/');
 $ch_2 = curl_init('http://www.baidu.com/');
 curl_setopt($ch_1, CURLOPT_RETURNTRANSFER, true);
 curl_setopt($ch_2, CURLOPT_RETURNTRANSFER, true);

 // build the multi-curl handle, adding both $ch
 $mh = curl_multi_init();
 curl_multi_add_handle($mh, $ch_1);
 curl_multi_add_handle($mh, $ch_2);

 // execute all queries simultaneously, and continue when all are complete
 $running = null;
 do {
     curl_multi_exec($mh, $running);
     $ch = curl_multi_select($mh);
     if($ch !== 0){
         $info = curl_multi_info_read($mh);
         if($info){
             var_dump($info);
             $response_1 = curl_multi_getcontent($info['handle']);
             echo "$response_1 \n";
             break;
         }
     }
 } while ($running > 0);

//close the handles
curl_multi_remove_handle($mh, $ch_1);
curl_multi_remove_handle($mh, $ch_2);
curl_multi_close($mh);
