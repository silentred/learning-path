<?php

$array = ['name'=>'dog', 'cat', 'snake'];
//echo array_shift($array) . '\n';

//print_r($array);

print_r(array_chunk($array, 2, true));

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
		echo "__destructing the object \n";
	}

	function __toString(){
		return "Person to string";
	}
}

$p = new Person();
print_r($p->name . "\n");
print_r($p. "\n");

$a = ['a', 'b', 'c'];
$index = array_search('b', $a);
array_splice($a, 1,1);
print_r("\n the index of b is ".$index . "\n");
print_r($a);



