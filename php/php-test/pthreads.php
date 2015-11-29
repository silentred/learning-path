<?php
class WorkerThread extends Thread {
public function __construct($i){
  $this->i=$i;
}

public function run(){
  while(true){
   echo $this->i;
   sleep(1);
  }
}
}

for($i=0;$i<10;$i++){
    $workers[$i]=new WorkerThread($i);
    $workers[$i]->start();
}
