<?php

require_once 'phpThumb/ThumbLib.inc.php';
ini_set("gd.jpeg_ignore_warning", 1);
ini_set("memory_limit",'512M');
function getPath($file){
	$index = strrpos($file, '/');
	return substr($file, 0, $index+1);
}

function makeDir($dir){
	if(!file_exists($dir)){
			mkdir($dir, 0766, true);
	}
}

$size_limit = array(
	[360, 600],[450,450], [330,600], [200,200], [190,190],[800,0],[219, 600], [219,300], [315, 197],[150, 150],[200,130],[335, 205],[335,700],[192, 120],[256, 170]
);


$PATH = '/home/case/7kk/sites/pic';
$width = intval($_GET['w']);
$height = intval($_GET['h']);
$path = $_GET['p'];
$type = intval($_GET['t']);

if(empty($path) or empty($type)){
echo "param invalid";    
exit(1);
}

$new_size = array($width, $height);
if(!in_array($new_size, $size_limit)){
echo "size invalid, no cache..";	
exit(1);
}

$originalFile = $PATH.'/upload'.$path;
$destFile = $PATH.'/simg/'.$type.'/'.$width.'_'.$height.$path;
//var_dump($destFile);exit;

if(!file_exists($destFile) and file_exists($originalFile)){
	$thumb = PhpThumbFactory::create($originalFile, ['jpegQuality'=>85]);
	switch($type){
		case 1:
			if($height==0){
				$thumb->resize($width);
			}else{
				$thumb->resize($width, $height);	
			}
			break;
		case 2:
			$thumb->adaptiveResize($width, $height);
			break;
	}
	makeDir(getPath($destFile));
//	$thumb->setOptions(['jpegQuality'=>85]);
	$thumb->save($destFile, $thumb->getFormat());
	$thumb->show();
	exit(0);
}

echo "Error";
exit(1);