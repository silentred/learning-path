<?php

$lock = new SyncSemaphore("UniqueName", 2);

for($i=0; $i<2; $i++){
	$pid = pcntl_fork();
	if($pid <0){
		die("fork failed");
	}elseif ($pid>0){
		echo "parent process \n";
	}else{
		echo "child process {$i} is born. \n";
		obtainLock($lock, $i);
	}
}

while (pcntl_waitpid(0, $status) != -1) { 
	$status = pcntl_wexitstatus($status); 
	echo "Child $status completed\n"; 
}

function obtainLock ($lock, $i){
	echo "process {$i} is getting the lock \n";
	$res = $lock->lock(200);
	sleep(1);
	if (!$res){
		echo "process {$i} unable to lock lock. \n";
	}else{
		echo "process {$i} successfully got the lock \n";
		$lock->unlock();
	}
	exit();
}



