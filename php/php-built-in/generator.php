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



function gen() {
    $ret = (yield 'yield1');
    var_dump($ret. " | in gen()");
    $ret = (yield 'yield2');
    var_dump($ret. " | in gen()");
}
 
$gen = gen();
var_dump($gen->rewind()); 
var_dump($gen->current());    // string(6) "yield1"
var_dump($gen->send('ret1')); // string(4) "ret1"   (the first var_dump in gen)
                              // string(6) "yield2" (the var_dump of the ->send() return value)
var_dump($gen->send('ret2')); 


class Task {
    protected $taskId;
    protected $coroutine;
    protected $sendValue = null;
    protected $beforeFirstYield = true;
 
    public function __construct($taskId, Generator $coroutine) {
        $this->taskId = $taskId;
        $this->coroutine = $coroutine;
    }
 
    public function getTaskId() {
        return $this->taskId;
    }
 
    public function setSendValue($sendValue) {
        $this->sendValue = $sendValue;
    }
 
    public function run() {
        if ($this->beforeFirstYield) {
            $this->beforeFirstYield = false;
            return $this->coroutine->current();
        } else {
            $retval = $this->coroutine->send($this->sendValue);
            $this->sendValue = null;
            return $retval;
        }
    }
 
    public function isFinished() {
        return !$this->coroutine->valid();
    }
}

class Scheduler {
    protected $maxTaskId = 0;
    protected $taskMap = []; // taskId => task
    protected $taskQueue;
 
    public function __construct() {
        $this->taskQueue = new SplQueue();
    }
 
    public function newTask(Generator $coroutine) {
        $tid = ++$this->maxTaskId;
        $task = new Task($tid, $coroutine);
        $this->taskMap[$tid] = $task;
        $this->schedule($task);
        return $tid;
    }
 
    public function schedule(Task $task) {
        $this->taskQueue->enqueue($task);
    }
 
    public function run() {
        while (!$this->taskQueue->isEmpty()) {
            $task = $this->taskQueue->dequeue();
            $task->run();
 
            if ($task->isFinished()) {
                unset($this->taskMap[$task->getTaskId()]);
            } else {
                $this->schedule($task);
            }
        }
    }
}

class SystemCall {
    protected $callback;
 
    public function __construct(callable $callback) {
        $this->callback = $callback;
    }
 
    public function __invoke(Task $task, Scheduler $scheduler) {
        $callback = $this->callback;
        return $callback($task, $scheduler);
    }
}