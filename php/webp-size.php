<?php

public static function imageSize($filename)
{
    $info = getimagesize($filename);
    if ($info) {
        list($width, $height) = $info;
        return [$width, $height];
    } else {
        return self::webpDimention($filename);
    }
}

public static function webpDimention($filename)
{
    $result = [null, null];

    $file = fopen($filename, 'r');
    $header = fread($file, 4); // riff
    if ($header !== 'RIFF') {
        return $result;
    }

    $chunkSize = fread($file, 4);
    $chunkSize = unpack('V', $chunkSize); // size, 4 bytes

    $webp = fread($file, 4); // WEBP

    $fourcc = fread($file, 4); // VP8X, VP8 , VP8L

    if ($fourcc == 'VP8X') {
        $sizeAndReserved = fread($file, 8);

        $b1 = fread($file, 1);
        $b2 = fread($file, 1);
        $b3 = fread($file, 1);
        $b4 = fread($file, 1);
        $b5 = fread($file, 1);
        $b6 = fread($file, 1);

        $w = ord($b3) << 16 | ord($b2) << 8 | ord($b1);
        $h = ord($b6) << 16 | ord($b5) << 8 | ord($b4);

        $result = [$w + 1, $h + 1];

    } elseif ($fourcc == 'VP8 ') {
        $sign = fread($file, 10);

        $w = fread($file, 2);
        $w = unpack('S', $w)[1] & 0x3fff;

        $h = fread($file, 2);
        $h = unpack('S', $h)[1] & 0x3fff;

        $result = [$w + 1, $h + 1];

    } elseif ($fourcc == 'VP8L') {
        $size = fread($file, 5);

        $b1 = ord(fread($file, 1));
        $b2 = ord(fread($file, 1));
        $b3 = ord(fread($file, 1));
        $b4 = ord(fread($file, 1));

        // 14 bits for width
        $widthMinusOne = ($b2 & 0x3F) << 8 | $b1;
        $heightMinusOne = ($b4 & 0x0F) << 10 | $b3 << 2 | $b2 >> 6;


        $result = [($widthMinusOne + 1), ($heightMinusOne + 1)];
    }

    return $result;
}