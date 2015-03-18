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