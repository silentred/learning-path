<?php

class Foo extends Stackable { 
	public $counter; 
	public function __construct(){ 
		$this->counter = 0; 
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
		while ($this->object->counter < 10){ 
			print $this->object->counter++." - {$this->text}\n"; 
			sleep(1); 
		} 
	} 
} 

$foo = new Foo(); 

$a = new Process("A",$foo); 
$a->start(); 

$b = new Process("B",$foo); 
$b->start();