<?php

//A single-frame unmasked text message
$data = array(0x81, 0x05, 0x48, 0x65, 0x6c, 0x6c, 0x6f);
//A single-frame masked text message
$data2 = array(0x81, 0x85, 0x37, 0xfa, 0x21, 0x3d, 0x7f, 0x9f, 0x4d, 0x51, 0x58);


handleData(toString($data));
handleData(toString($data2));

function toString(array $data) {
    return array_reduce($data, function($carry, $item){
        return $carry .= chr($item);
    });
}

function handleData($data){
	$offset = 0;

	$temp = ord($data[$offset++]);
	$FIN = ($temp >> 7) & 0x1;
	$RSV1 = ($temp >> 6) & 0x1;
	$RSV2 = ($temp >> 5) & 0x1;
	$RSV3 = ($temp >> 4) & 0x1;
	$opcode = $temp & 0xf;

	echo "First byte: FIN is $FIN, RSV1-3 are $RSV1, $RSV2, $RSV3; Opcode is $opcode \n";

	$temp = ord($data[$offset++]);
	$mask = ($temp >> 7) & 0x1;
	$payload_length = $temp & 0x7f;
	if($payload_length == 126){
		$temp = substr($data, $offset, 2);
		$offset += 2;
		$temp = unpack('nl', $temp);
		$payload_length = $temp['l'];
	}elseif($payload_length == 127){
		$temp = substr($data, $offset, 8);
		$offset += 8;
		$temp = unpack('nl', $temp);
		$payload_length = $temp['l'];
	}
	echo "mask is $mask, payload_length is $payload_length \n";

	if($mask ==0){
		$temp = substr($data, $offset);
		$content = '';
        for ($i=0; $i < $payload_length; $i++) { 
            $content .= $temp[$i];
        }
	}else{
		$masking_key = substr($data, $offset, 4);
		$offset += 4;
		
		$temp = substr($data, $offset);
		$content = '';
        for ($i=0; $i < $payload_length; $i++) { 
            $content .= chr(ord($temp[$i]) ^ ord($masking_key[$i%4]));
        }
	}

	echo "content is $content \n";
}

