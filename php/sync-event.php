<?php

for($i=0; $i<3; $i++){
	$pid = pcntl_fork();
	if($pid <0){
		die("fork failed");
	}elseif ($pid>0){
		//echo "parent process \n";
	}else{
		echo "child process {$i} is born. \n";
		switch ($i) {
		case 0:
			wait();
			break;
		case 1:
			wait();
			break;
		case 2:
			sleep(1);
			fire();
			break;
		}
	}
}

while (pcntl_waitpid(0, $status) != -1) { 
	$status = pcntl_wexitstatus($status); 
	echo "Child $status completed\n"; 
}

function wait(){
	$event = new SyncEvent("UniqueName");
	echo "before waiting. \n";
	$event->wait();
	echo "after waiting. \n";
	exit();
}

function fire(){
	$event = new SyncEvent("UniqueName");
	$event->fire();
	exit();
}