<?php
function find_node($key, &$node){
    $item = $node[$key];
    return $item;
}
$tree = array('one', 'two', 'three', 'four');
$item = &find_node(3, $tree);
$item = 'new value';
var_dump($item);