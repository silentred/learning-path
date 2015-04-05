<?php

function ajustArray(array &$a, $l, $r)
 {
 	$i = $l;
 	$j = $r;
 	$x = $a[$i];

 	while ( $i < $j ) {
 		//from right to left, searching the item smaller than X, then put it into the left side.
 		//until $i == $j
 		while ( $i < $j && $a[$j] > $x) {
 			$j--;	
 		}
 		if($i < $j){
 			$a[$i] = $a[$j];
 			$i++;
 		}
 		
 		//from left to right, searching the item bigger than X, then put it into right side,
 		//until $ == $j
 		while ( $i < $j && $a[$i] < $x) {
 			$i++;
 		}
 		if($i < $j){
 			$a[$j] = $a[$i];
 			$j--;
 		}
 		
 	}
 	//put X into the hole when $i==$j
 	$a[$i] = $x;
 	return $i;
 } 

function _quickSort(array &$a, $l, $r){
 	if ($l < $r) {
 		$i = ajustArray($a, $l, $r);
 		_quickSort($a, $l, $i -1 );
 		_quickSort($a, $i+1, $r);
 	}
 
 }

 function quickSort(array &$a, $l, $r)
 {
 	if ($l < $r) {
 		$i = $l; $j = $r; $x = $a[$i];
 		while ( $i < $j ) {
	 		while ( $i < $j && $a[$j] > $x)
	 			$j--;
	 		if($i < $j){
	 			$a[$i++] = $a[$j];
	 		}
	 		
	 		while ( $i < $j && $a[$i] < $x)
	 			$i++;
	 		if($i < $j){
	 			$a[$j++] = $a[$i];
	 		}
	 	}
	 	$a[$i] = $x;
	 	quickSort($a, $l, $i -1);
	 	quickSort($a, $i+1, $r);
 	}
 }



 function reverseQuickSort(array &$a, $l, $r)
 {
 	if ($l < $r) {
 		$i = $l; $j = $r; $x = $a[$i];
 		while ( $i < $j ) {
	 		while ( $i < $j && $a[$j] < $x)
	 			$j--;
	 		if($i < $j){
	 			$a[$i++] = $a[$j];
	 		}
	 		
	 		while ( $i < $j && $a[$i] > $x)
	 			$i++;
	 		if($i < $j){
	 			$a[$j++] = $a[$i];
	 		}
	 	}
	 	$a[$i] = $x;
	 	reverseQuickSort($a, $l, $i -1);
	 	reverseQuickSort($a, $i+1, $r);
 	}
 }

 $array = [23,43,3,12,54,65,26,32,16,43,54,59];
 reverseQuickSort($array, 0, count($array)-1);
 var_dump($array);


 $array = [23,43,3,12,54,65,26,32,16,43,54,59];
 quickSort($array, 0, count($array)-1);
 var_dump($array);

