<?php

function swap(&$a, &$b)
{
	$temp = $b;
	$b = $a;
	$a = $temp;
}

function minHeapFixup(array &$a , $i){
	for ($j = (int)(($i-1)/2); ( $j>=0 && $i!=0 && $a[$i]<$a[$j] ); $i=$j, $j=(int)(($i-1)/2)) { 
		swap($a[$i], $a[$j]);
	}

	/*$j = (int)(($i-1)/2); 
	while ( $j>=0 && $i!=0 && $a[$i]<$a[$j] ) {
		swap($a[$i], $a[$j]);
		$i=$j; $j=(int)(($i-1)/2);
	}*/

}

function addNumber(array &$a, $i, $value){
	$a[$i] = $value;
	minHeapFixup($a, $i);
}
/*
$a = 1, $b = $a+1;
var_dump($b);*/

$array = [2,4,6];
addNumber($array, 3, 1);
var_dump($array);