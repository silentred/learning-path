<?php

$key = ftok('/tmp', 'c');
$sem = sem_get($key);

for($i=0; $i<2; $i++){
	$pid = pcntl_fork();
	if($pid <0){
		die("fork failed");
	}elseif ($pid>0){
		//echo "parent process \n";
	}else{
		echo "child process {$i} is born. \n";
		obtainLock($sem, $i);
	}
}

while (pcntl_waitpid(0, $status) != -1) { 
	$status = pcntl_wexitstatus($status); 
	echo "Child $status completed\n"; 
}
sem_remove($sem); // finally remove the sem

function obtainLock ($sem, $i){
	echo "process {$i} is getting the sem \n";
	$res = sem_acquire($sem, true);
	sleep(1);
	if (!$res){
		echo "process {$i} unable to get sem. \n";
	}else{
		echo "process {$i} successfully got the sem \n";
		sem_release($sem);
	}
	exit();
}