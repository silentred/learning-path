<?php

function xrange($start, $end, $step = 1) {
    for ($i = $start; $i <= $end; $i += $step) {
        yield $i;
    }
}

$gen = xrange(1, 10);
foreach ($gen as $num) {
    echo $num, "\n";
}