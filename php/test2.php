<?php

$arr = array('a'=>'first', 'b'=>'second', 'c'=>'third');
var_dump(current($arr));
foreach ($arr as &$a); // do nothing. maybe?
xdebug_debug_zval('a');
xdebug_debug_zval('arr');//这时，$arr['c']有两个引用，且is_ref=1
var_dump(current($arr));
//unset($a); //这里unset以下就正常了
// 当 foreach 开始执行时，数组内部的指针会自动指向第一个单元。这意味着不需要在 foreach 循环之前调用 reset()。
// 这里有个坑，说明了unset($a)的重要性：
// 此时，$a是一个引用指向$arr['c'],就是说$arr['c']的is_ref为1
// 开始foreach循环，猜测, 第一个赋值 $a = $arr['a'], $a为左值，此时$a指向的数据为引用，所以，直接改变其值，把'first'赋给了$arr['c']
// 第二个赋值 $a = $arr['b'], 此时$arr['c']变成了'second'
// 第三次赋值 不用解释了，这里的整个过程，$a都是一个指向$arr['c']的引用，所以才会出现这种错误
echo "\nstart second foreach:\n";
foreach ($arr as $a){
    xdebug_debug_zval('arr');
    echo "current index is: ".current($arr)."\n";
    xdebug_debug_zval('a');
};  
xdebug_debug_zval('arr');
print_r($arr);



class Test {
    public $hello;
}
//参数不带&，只能改变object的property，没办法改变obj本身
function modify($obj) { $obj->hello = 'world (modified)!'; }
// 只有显示的 对参数 加上&（ampersand）,才能改变obj本身
function modify2($obj) { $obj = 32; }
$obj = new Test();
$obj->hello = 'world';
modify($obj);
modify2($obj);
var_dump($obj->hello);  // outputs "world (modified!)"



// Example one
$arr1 = array(1);
echo "\nbefore:\n";
echo "\$arr1[0] == {$arr1[0]}\n";
$arr2 = $arr1;
$arr2[0]++;
echo "\nafter:\n";
echo "\$arr1[0] == {$arr1[0]}\n";
echo "\$arr2[0] == {$arr2[0]}\n";

// Example two
echo "\nExample2:\n";
$arr3 = array(1);
xdebug_debug_zval('arr3');
$a =& $arr3[0];//$arr3的is_ref变为1
echo "\nbefore:\n";
echo "\$a == $a\n";
echo "\$arr3[0] == {$arr3[0]}\n";
xdebug_debug_zval('a');
xdebug_debug_zval('arr3');
$arr4 = $arr3;
xdebug_debug_zval('arr3');
xdebug_debug_zval('arr4');
$arr4[0]++; //这时候$arr4[0]指向了$arr3[0],而$arr3[0]由于上面的&操作，其is_ref变为了1, 所以这里改变的是$arr3[0]的值
$arr4[1] = 2;//$arr4并非引用，所以添加元素不影响$arr3
echo "\nafter:\n";
echo "\$a == $a\n";
echo "\$arr3[0] == {$arr3[0]}\n";
echo "\$arr4[0] == {$arr4[0]}\n";
var_dump($arr4);
var_dump($arr3);



function find_node($key, &$node){
    $item = &$node[$key];
    return $item;
}
$tree = array('one', 'two', 'three', 'four');
$item = &find_node(3, $tree);
$item = 'new value';
var_dump($item);