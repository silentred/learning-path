<?php

$arr = array('a'=>'first', 'b'=>'second', 'c'=>'third');
var_dump(current($arr));
foreach ($arr as &$a); // do nothing. maybe?
//xdebug_debug_zval('a');
//xdebug_debug_zval('arr');//这时，$arr['c']有两个引用，且is_ref=1
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
    //xdebug_debug_zval('arr');
    echo "current index is: ".current($arr)."\n";
    //xdebug_debug_zval('a');
};  
//xdebug_debug_zval('arr');
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
//xdebug_debug_zval('arr3');
$a =& $arr3[0];//$arr3的is_ref变为1
echo "\nbefore:\n";
echo "\$a == $a\n";
echo "\$arr3[0] == {$arr3[0]}\n";
//xdebug_debug_zval('a');
//xdebug_debug_zval('arr3');
$arr4 = $arr3;
//xdebug_debug_zval('arr3');
//xdebug_debug_zval('arr4');
$arr4[0]++; //这时候$arr4[0]指向了$arr3[0],而$arr3[0]由于上面的&操作，其is_ref变为了1, 所以这里改变的是$arr3[0]的值
$arr4[1] = 2;//$arr4并非引用，所以添加元素不影响$arr3
echo "\nafter:\n";
echo "\$a == $a\n";
echo "\$arr3[0] == {$arr3[0]}\n";
echo "\$arr4[0] == {$arr4[0]}\n";
var_dump($arr4);
var_dump($arr3);


/*
这里的&$node[$key]的&必须存在，或者直接return $node[$key]也可以，不能通过非引用中间变量$item返回，不知道为什么
 */
function &find_node($key, &$node){
    //xdebug_debug_zval('node');
    $item = &$node[$key]; //这里的&不能省略，原因如下：
    /*这里如果省去&，$item和$node[$key]虽然指向同一个zval，但是return的时候会有问题，因为php引用赋值的一个特点，如下。
    $a = 1; $b = $a; $c = &$b; 这里第三步的时候，会复制一个zval（int 1），$c和$b指向他，而$a还是指向最开始的那个zval。
    好了，当return $item; $item = &find_node()的时候，由于$item不是一个引用，便会复制一个zval，函数中的item和全局变量item都指向他，但是函数结束后，function中的symbol全部被unset，这时刚才创建的zval便只剩下一个引用refcount=1，所以他的is_ref会被设为0。
    */
    //xdebug_debug_zval('node');
    //xdebug_debug_zval('item');
    return $item;
}
$tree = array('one', 'two', 'three', 'four');
$item = &find_node(3, $tree);
//xdebug_debug_zval('item');
//xdebug_debug_zval('tree');
$item = 'new value';
var_dump($tree[3]);


/*
函数返回引用的时候，必须在定义和使用的时候都加上&，这点和参数传入引用不同
 */
function &func(){
    static $static = 0;
    $static++;
    return $static;
}

$var1 =& func();
//xdebug_debug_zval('var1');
echo "var1:", $var1; // 1
func();
func();
echo "var1:", $var1; // 3
$var2 = func(); // assignment without the &
echo "var2:", $var2; // 4
func();
func();
echo "var1:", $var1; // 6
echo "var2:", $var2; // still 4


//和js中的效果不一样，赋值运算优先于or；||优先于赋值运算，所以如果这里用||代替or，则$a结果为true
$a = 0 or 19;
var_dump($a);

// Example to parse "PUT" requests 
$a = file_get_contents('php://input');
$b = file_get_contents('file:///home/jason/test.txt');
//$c = file_get_contents(STDIN);
// The result
var_dump($a);
print_r($b);
//var_dump($c);

foreach (glob("/home/jason/*.txt") as $filename) {
    echo "$filename size " . filesize($filename) . "\n";
}

//查看默认报错级别
var_dump(error_reporting());

$stdin = fopen('php://stdin', 'r');
echo "$stdin \n";


//popen用来调用系统的命令，他的io pipe是单向的（只能读或者写）
//返回一个文件指针（file pointer）, 和fopen()一样,但是fopen是双向io。
//必须用pclose()关闭资源
//This pointer may be used with fgets(), fgetss(), and fwrite()
$handle = popen('ls -al /', 'r');
$contents = '';
/* 读取内容 方法一 
while (!feof($handle)) {
  $contents .= fread($handle, 512);
  echo 'current point is at'.ftell($handle). "\n";
}*/
/*读取内容 方法二*/
$contents = stream_get_contents($handle);

/*file_get_contents($filename); 参数是文件名， 而stream_get_contents读取的是一个已经打开的资源，所以file_get_contents在这里不适用*/
pclose($handle);
echo $contents . "\n";


declare(ticks=1);
// A function called on each tick event
function tick_handler()
{
    echo "tick_handler() called\n";
}

register_tick_function('tick_handler');

$a = 1;

if ($a > 0) {
    $a += 2;
    print($a."\n");
}