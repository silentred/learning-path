<?php

$pid_file = "/tmp/process.pid";
$pid = posix_getpid();
$fp = fopen($pid_file, 'w+');
if(flock($fp, LOCK_EX)){
	echo "got the lock \n";
	ftruncate($fp, 0);      // truncate file
    fwrite($fp, $pid);
    fflush($fp);            // flush output before releasing the lock
    flock($fp, LOCK_UN);    // 释放锁定
} else {
	echo "Cannot get pid lock. The process is already up \n";
}
fclose($fp);


declare(ticks = 1);
// signal handler function
function sig_handler($signo){
	switch ($signo) {
	case SIGTERM:
		echo "Caught SIGTERM...\n";
		// handle shutdown tasks
		exit;
		break;
	case SIGHUP:
		echo "Caught SIGHUP...\n";
		// handle restart tasks
		break;
	case SIGUSR1:
		echo "Caught SIGUSR1...\n";
		break;
	case SIGINT:
		echo "keyboard interrupt..\n";
		break;
	default:
		// handle all other signals
	}
}

echo "Installing signal handler...\n";

// setup signal handlers
pcntl_signal(SIGTERM, "sig_handler");
pcntl_signal(SIGHUP,  "sig_handler");
pcntl_signal(SIGUSR1, "sig_handler");
pcntl_signal(SIGINT, "sig_handler");
// or use an object, available as of PHP 4.3.0
// pcntl_signal(SIGUSR1, array($obj, "do_something"));

echo"Generating signal SIGUSR1 to self...\n";

// send SIGUSR1 to current process id
// posix_* functions require the posix extension
posix_kill(posix_getpid(), SIGUSR1);
sleep(1);

echo "Done\n";


// IPC shared memory
$shm_key = ftok(__FILE__, 't');
$shm_id = shmop_open($shm_key, "c", 0644, 100);
shmop_close($shm_key);

// multi process


