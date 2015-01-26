<?php
function resize($originalFile, $outputFile) {
	$info = getimagesize($originalFile);
    $mime = $info['mime'];
    $bgWidth = 270;
    $bgHeight = 270;

    switch ($mime) {
            case 'image/jpeg':
                    $image_create_func = 'imagecreatefromjpeg';
                    $image_save_func = 'imagejpeg';
                    $new_image_ext = 'jpg';
                    break;

            case 'image/png':
                    $image_create_func = 'imagecreatefrompng';
                    $image_save_func = 'imagepng';
                    $new_image_ext = 'png';
                    break;

            case 'image/gif':
                    $image_create_func = 'imagecreatefromgif';
                    $image_save_func = 'imagegif';
                    $new_image_ext = 'gif';
                    break;

            default: 
                    throw Exception('Unknown image type.');
    }

    $img = $image_create_func($originalFile);

    list($width, $height) = getimagesize($originalFile);
    if (($width-$bgWidth) >= ($height-$bgHeight)) {
    	$newWidth = $bgWidth;
    	$newHeight = ($height/$width)*$newWidth;
    	$dst_x = 0;
    	$dst_y = ($bgHeight-$newHeight)/2;
    }elseif (($width-$bgWidth) < 0 && ($height-$bgHeight)<0) {
    	$newWidth = $width;
    	$newHeight = $height;
    	$dst_x = ($bgWidth-$width)/2;
    	$dst_y = $dst_y = ($bgHeight-$newHeight)/2;
    }else{
    	throw new Exception("Error on deciding newWidth", 1);
    }

    $bg = imagecreatetruecolor($bgWidth, $bgHeight);
    imagefill($bg, 0, 0, imagecolorallocate($bg, 255, 255, 255));

    imagecopyresampled($bg, $img, $dst_x, $dst_y, 0, 0, $newWidth,
    	 $newHeight, $width, $height);

    if (file_exists($outputFile)) {
            unlink($outputFile);
    }
    $image_save_func($bg, $outputFile);
    imagedestroy($bg);
    imagedestroy($img);	

}

$fileDir = '/home/jason/projects/product-img/';
$outDir = '/home/jason/projects/product-img/resized/';
$files = scandir($fileDir);
foreach($files as $file){
	if(is_file($fileDir.$file)){
		print_r("Processing $file \n");
		$inputFile = $fileDir.$file;
		$info = pathinfo($file);
		$outputFile = $outDir.$info['filename']. '.png';
		
		if(isset($info['extension']) && $info['extension'] == 'png'){
			resize($inputFile, $outputFile);
		}
	}
}


