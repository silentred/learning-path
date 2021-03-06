<?php

class Foo extends Stackable { 
	public $url;
	public $response = null;
	public function __construct(){ 
		$this->url = 'http://www.baidu.com'; 
	} 
	public function run(){} 
} 

class Process extends Worker { 
	private $text = ""; 
	public function __construct($text,$object){ 
		$this->text = $text; 
		$this->object = $object; 
	} 
	public function run(){
		while (is_null($this->object->response)){ 
			print " Thread {$this->text} is running\n"; 
			$this->object->response = 'http response';
			sleep(1); 
		} 
	} 
} 

$foo = new Foo(); 

$a = new Process("A",$foo); 
$a->start(); 

$b = new Process("B",$foo); 
$b->start();
echo $foo->response;

