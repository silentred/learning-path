<?php

function mergeArray(array &$a, $first, $mid, $last, $temp)
 {
 	$i = $first; $j = $mid+1;
 	$m = $mid; $n = $last;
 	$k = 0;

 	while ($i <= $m && $j <= $n) {
 		if ($a[$i] <= $a[$j] ) {
 			$temp[$k++] = $a[$i++];
 		}else{
 			$temp[$k++] = $a[$j++];
 		}
 	}

 	while ($i <= $m) {
 		$temp[$k++] = $a[$i++];
 	}

 	while ($j <= $n) {
 		$temp[$k++] = $a[$j++];
 	}

 	for ($i=0; $i < $k; $i++) { 
 		$a[$first + $i] = $temp[$i];
 	}
 } 

function mergeSort(array &$a, $first, $last, $temp)
{
	if($first < $last){
		$mid = (int)(($first+$last)/2);
		mergeSort($a, $first, $mid, $temp);
		mergeSort($a, $mid+1, $last, $temp);
		mergeArray($a, $first, $mid, $last, $temp);
	}
	
}

 $array = [23,43,3,12,54,65,26,32,16,43,54,59];
 mergeSort($array, 0, count($array)-1, [] );
 var_dump($array);