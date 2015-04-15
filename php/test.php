<?php
$array = array('name'=>'dog', 'cat', 'snake');
//echo array_shift($array) . '\n';
//print_r($array);

//print_r(array_chunk($array, 2, true));

class Person{
	public function __get($property)
	{
		$methed = "get{$property}";
		echo $methed;
		if (method_exists($this, $methed)) {
			return $this->$methed();
		}
	}

	function getName(){
		return "Bob";
	}

	function getAge(){
		return 44;
	}

	function __destruct(){
		echo "\n __destructing the object \n";
	}

	function __toString(){
		return "Person to string";
	}
}

$p = new Person();
print_r($p->name . "\n");
print_r($p. "\n");

$a = array('a', 'b', 'c');
$index = array_search('b', $a);
array_splice($a, 1,1);
print_r("\n the index of b is ".$index . "\n");
print_r($a);

$a = 'cd';
$$a='hello ';
$$a .= 'world';
print_r($cd);

echo "\ntest==0 result is \n";
print_r('test'==0);
echo "\n";

//for($i=1; $i<=9; $i++){
//	for($j=1;$j<=$i;$j++){
//		echo "$j x $i = ".$j*$i."  ";
//	}
//	echo "\n";
//}

$today = strtotime(date("Y-m-d"));
$date = strtotime('2014-10-10');
$days = round(($today-$date)/3600/24);
echo $days, "\n";

echo pack("HH", 45, 51);

echo "\n reverse string start \n ";

$start = microtime();
$string = "hello world";
$result;
for($i=100000;$i--;){
	$a = str_split($string);
	$result = join('',array_reverse($a));
}
$end = microtime();
echo "$result, processed for ", ($end-$start), " ms";

$array = array();
//echo $array['no']['existing']; 这里会提示PHP Notice:  Undefined index

$instance = new stdClass();
//echo $instance->no_existing; 这里会提示PHP Notice:  Undefined property:


//Laravel的模板输出用的方式，先打开输出缓存，echo 输出内容，最后get到变量里
/*
$level = ob_get_level(); //0
ob_start();
//$level = ob_get_level();//1
include "include-me.php";
$content = ob_get_clean();
echo "\n!!!This is a cache, not direct output!! OB_LEVEL={$level}\n".$content;

echo "\n".urlencode('http://sss.sss.com/!@#%$^&喜剧');
*/


//不对称加密，需要安装openssl扩展
class MyEncryption
{

    public $pubkey;
    public $privkey ;

    public function __construct(){
    	$config = array(
	    "digest_alg" => "sha512",
	    "private_key_bits" => 4096,
	    "private_key_type" => OPENSSL_KEYTYPE_RSA,
	);
    	// Create the private and public key
	$res = openssl_pkey_new($config);
	// Extract the private key from $res to $privKey
	openssl_pkey_export($res, $privKey);
	// Extract the public key from $res to $pubKey
	$pubKey = openssl_pkey_get_details($res);
	$pubKey = $pubKey["key"];

    	$this->privkey = $privKey;
    	$this->pubkey = $pubKey;
    }

    public function encrypt($data)
    {
        if (openssl_public_encrypt($data, $encrypted, $this->pubkey))
            $data = base64_encode($encrypted);
        else
            throw new Exception('Unable to encrypt data. Perhaps it is bigger than the key size?');

        return $data;
    }

    public function decrypt($data)
    {
        if (openssl_private_decrypt(base64_decode($data), $decrypted, $this->privkey))
            $data = $decrypted;
        else
            $data = '';

        return $data;
    }
}

$hasher = new MyEncryption();
$encryptData = $hasher->encrypt('hello world');
//echo "\n public key : {$hasher->pubkey} \n";
//echo "\n public key : {$hasher->privkey} \n";
echo "\n". $encryptData;
$decryptData = $hasher->decrypt($encryptData);
echo "\n". $decryptData;



/*for ($i = 1; $i <= 5; ++$i) { 
    $pid = pcntl_fork(); 

    if (!$pid) { 
        sleep(1); 
        print "In child $i\n"; 
        exit($i); 
    } 
} 

while (pcntl_waitpid(0, $status) != -1) { 
    $status = pcntl_wexitstatus($status); 
    echo "Child $status completed\n"; 
} */

echo "\n msg_get_queue exists: ".function_exists('msg_get_queue');


$users = array(
    array('name' => 'tom', 'age' => 20)
    , array('name' => 'anny', 'age' => 18)
    , array('name' => 'jack', 'age' => 22)
);
usort($users, function($a, $b) {
            $al = $a['age'];
            $bl = $b['age'];
            if ($al == $bl)
                return 0;
            return ($al > $bl) ? -1 : 1;
        });
var_dump($users);



// array_reduce(input, function)的简介
// Laravel的责任链的实现方式就用了这个函数
$arr = array( 
    array('min' => 1.5456, 'max' => 2.28548, 'volume' => 23.152), 
    array('min' => 1.5457, 'max' => 2.28549, 'volume' => 23.152), 
    array('min' => 1.5458, 'max' => 2.28550, 'volume' => 23.152), 
    array('min' => 1.5459, 'max' => 2.28551, 'volume' => 23.152), 
    array('min' => 1.5460, 'max' => 2.28552, 'volume' => 23.152), 
); 

$initial = array_shift($arr); 

$t = array_reduce($arr, function($result, $item) { 
    $result['min'] = min($result['min'], $item['min']); 
    $result['max'] = max($result['max'], $item['max']); 
    $result['volume'] += $item['volume']; 

    return $result; 
}, $initial); 
var_dump($t);

//例2, 打印的两个值是相同的
function f($v,$w){return "f($v,$w)";}
var_dump(array_reduce(array(1,2,3,4), 'f', 99 ));
var_dump(array_reduce(array(2,3,4), 'f',  f(99,1) ));
//他的php实现大致是这样：把上一个reduce的结果作为callback的第一个参数，每一个数组中的元素迭代作为第二个参数；第一次执行callback的时候如果$inital没有指定，则为null
function my_array_reduce($array, $callback, $initial=null)
{
    $acc = $initial;
    foreach($array as $a)
        $acc = $callback($acc, $a);
    return $acc;
}

function time2($value)
{
    return $value*2;
}
$a = array(1,4,6,7);
var_dump(array_map(time2, $a));

//var_dump(empty(array()));


/*内存泄露：互相引用*/
class Foo {
    function __construct()
    {
        $this->bar = new Bar($this);
    }
}

class Bar {
    function __construct($foo = null)
    {
        $this->foo = $foo;
    }
}

/*while (true) {
    $foo = new Foo();
    unset($foo);
    echo number_format(memory_get_usage()) . "\n";
    sleep(1);
}*/

//array 的+号操作, 若有元素冲突，则以左侧的值为准，忽略右侧的值。
$a = array('a'=>'11', 'b'=>'22');
$b = array('b'=>'bb3', 'c'=>'cc4');
$new = $a+$b; //这里'b'的值为22
var_dump($new);



$regex = '/(?<=\{)[a-zA-z0-9_-]+(?=\})/';  /* d 前面紧跟c, d 后面紧跟e*/
$str = 'sdf/sdf/{type}-{location}-{year}---.html';
$matches = array();
if(preg_match_all($regex, $str, $matches)){
    var_dump($matches);
}


var_dump(date('Y-m-d h:i:s'));


// Reference
$var1 = "Example variable";
$var2 = "null";

function global_references($use_globals)
{
    global $var1, $var2;
    if (!$use_globals) {
        $var2 =& $var1; // visible only inside the function
    } else {
        $GLOBALS["var2"] =& $var1; // visible also in global context
    }
}
global_references(false);
echo "var2 is set to '{$var2}'\n"; // var2 is set to 'null'
global_references(true);
echo "var2 is set to '{$var2}'\n"; // var2 is set to 'Example variable'

