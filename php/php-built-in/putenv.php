<?php

$name = 'SESSION_DRIVER';
$value = 'file';
for ( $i=0; $i<1000000; $i++) {
    if (!putenv("$name=$value")) {
        echo "failed at $i \n";
    }
    if ($i %100000 === 0 ) {
        echo "$i... \n";
    }
}