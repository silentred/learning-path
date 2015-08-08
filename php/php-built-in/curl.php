<?php

function login_post($url, $cookie, $post) { 
    $curl = curl_init();//初始化curl模块 
    curl_setopt($curl, CURLOPT_URL, $url);//登录提交的地址 
    curl_setopt($curl, CURLOPT_HEADER, 0);//是否显示头信息 
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, 0);//是否自动显示返回的信息 
    curl_setopt($curl, CURLOPT_COOKIEJAR, $cookie); //设置Cookie信息保存在指定的文件中 
    curl_setopt($curl, CURLOPT_POST, 1);//post方式提交 
    curl_setopt($curl, CURLOPT_POSTFIELDS, http_build_query($post));//要提交的信息 
    curl_exec($curl);//执行cURL 
    curl_close($curl);//关闭cURL资源，并且释放系统资源 
} 

function get_content($url, $cookie) { 
    $ch = curl_init(); 
    curl_setopt($ch, CURLOPT_URL, $url); 
    curl_setopt($ch, CURLOPT_HEADER, 0); 
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
    curl_setopt($ch, CURLOPT_COOKIEFILE, $cookie); //读取cookie 
    $rs = curl_exec($ch); //执行cURL抓取页面内容 
    curl_close($ch); 
    return $rs; 
} 

//设置post的数据 
$post = array ( 
    'email' => 'oschina账户', 
    'pwd' => 'oschina密码', 
    'goto_page' => '/my', 
    'error_page' => '/login', 
    'save_login' => '1', 
    'submit' => '现在登录' 
); 
 
//登录地址 
$url = "https://www.oschina.net/home/login"; 
//设置cookie保存路径 
$cookie = dirname(__FILE__) . '/cookie_tmp.txt'; 
//登录后要获取信息的地址 
$url2 = "http://m.oschina.net/my"; 
//模拟登录 
login_post($url, $cookie, $post); 
//获取登录页的信息 
$content = get_content($url2, $cookie); 
//删除cookie文件 
@ unlink($cookie); 
//匹配页面信息 
$preg = "/<td class='portrait'>(.*)<\/td>/i"; 
preg_match_all($preg, $content, $arr); 
$str = $arr[1][0]; 
//输出内容 
echo $str; 