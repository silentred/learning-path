<?php
// descriptor array
$desc = array(
    0 => array('pipe', 'r'), // 0 is STDIN for process
    1 => array('pipe', 'w'), // 1 is STDOUT for process
    2 => array('file', '/tmp/error-output.txt', 'a') // 2 is STDERR for process
);

// command to invoke markup engine
$cmd = "cowsay";

// spawn the process
$p = proc_open($cmd, $desc, $pipes);

// send the wiki content as input to the markup engine 
// and then close the input pipe so the engine knows 
// not to expect more input and can start processing
fwrite($pipes[0], 'Hello World!');
fclose($pipes[0]);

// read the output from the engine
$say = stream_get_contents($pipes[1]);

// all done! Clean up
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($p);

echo $say;