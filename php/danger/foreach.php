<?php

function test_1(){
    $a = [1,2,4];
    var_dump(current($a));
    foreach($a as $v){
        var_dump(current($a));
    }
};
test_1();

function test_2(){
    $a = [1,2,4];
    $b = &$a;
    foreach($a as $v){
        var_dump(current($a));
    }
};
//test_2();

function test_3(){
    $a = [1,2,4];
    $b = $a;
    foreach($a as $v){
        var_dump(current($a));
    }
};
//test_3();