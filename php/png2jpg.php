<?php

// Quality is a number between 0 (best compression) and 100 (best quality)
function png2jpg($originalFile, $outputFile, $quality=50) {
    $image = imagecreatefrompng($originalFile);
	$bg = imagecreatetruecolor(imagesx($image), imagesy($image));
	imagefill($bg, 0, 0, imagecolorallocate($bg, 255, 255, 255));
	imagealphablending($bg, TRUE);
	imagecopy($bg, $image, 0, 0, 0, 0, imagesx($image), imagesy($image));
	imagedestroy($image);
	//$quality = 50; // 0 = worst / smaller file, 100 = better / bigger file 
	
	imagejpeg($bg, $outputFile, $quality);
	imagedestroy($bg);	
}

$fireDir = '/home/jason/projects/product-img/';
$files = scandir($fireDir);
foreach($files as $file){
	if(is_file($file)){
		$inputFile = $fireDir.$file;
		$info = pathinfo($file);
		$outputFile = $fireDir.$info['filename']. '.jpg';
		if(isset($info['extension']) && $info['extension'] == 'png'){
			png2jpg($inputFile, $outputFile, 100);
		}
	}
}

