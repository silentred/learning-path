<?php

$int = base_convert('11111000', 2, 10);
var_dump($int & 0xf);