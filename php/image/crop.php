<?php
//等比缩小图片，并截出中心的内容，大小为$destWidth, $destHieght, 保存到$destFile
function cropImage($origFile, $destFile, $destWidth, $destHieght, $quality=80){
    $image = imagecreatefromjpeg($origFile);

    $destWidth = 200;
    $destHieght = 200;

    $width = imagesx($image);
    $height = imagesy($image);

    $original_aspect = $width / $height;
    $thumb_aspect = $destWidth / $destHieght;

    if ( $original_aspect >= $thumb_aspect )
    {
       // If image is wider than thumbnail (in aspect ratio sense)
       $new_height = $destHieght;
       $new_width = $width / ($height / $destHieght);
    }
    else
    {
       // If the thumbnail is wider than the image
       $new_width = $destWidth;
       $new_height = $height / ($width / $destWidth);
    }

    $thumb = imagecreatetruecolor( $destWidth, $destHieght );
    // Resize and crop
    imagecopyresampled($thumb,
       $image,
       0 - ($new_width - $destWidth) / 2, // Center the image horizontally
       0 - ($new_height - $destHieght) / 2, // Center the image vertically
       0, 0,
       $new_width, $new_height,
       $width, $height);
    imagejpeg($thumb, $destFile, 80);
}

cropImage(__DIR__.'/1.jpg', __DIR__.'/1-crop.jpg', 200, 200);