<?php

$array = [23,43,3,12,54,65,26,32,16,43,54,59];

function insertion_sort($array){
	$n = count($array)-1; // last index
	// j from 1 to $n
	for($j=1; $j<=$n; $j++){
		// take out the $j;
		$out = $array[$j];
		// i from $j-1 to 0
		$i = $j-1;
		while($i>=0 && $array[$i]>$out){
			$array[$i+1] = $array[$i];
			$i--;
		}
		$array[$i+1] = $out;
	}
	return $array;
}

var_dump(insertion_sort($array));