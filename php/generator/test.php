<?php
use App\Scheduler;
use App\SystemCall;
use App\Task;

/**
 * Created by PhpStorm.
 * User: Jason
 * Date: 11/21/2015
 * Time: 11:20 PM
 */

require_once "vendor/autoload.php";

function xrange($start, $end, $step = 1) {
    for ($i = $start; $i <= $end; $i += $step) {
        $ret = (yield $i);
        echo "i is $i, ret is $ret \n";
    }
}

$range = xrange(1, 5);

var_dump($range->rewind());
/*var_dump($range->current());
var_dump($range->next());*/
//var_dump($range->current());
var_dump($range->send("test"));
var_dump($range->send("test2"));

/*foreach ($range as $num) {
    echo $num, "\n";
}*/

//var_dump($range); // object(Generator)#1
//var_dump($range instanceof Iterator); // bool(true)

echo "## Second Test \n";

function getTaskId() {
    return new SystemCall(function(Task $task, Scheduler $scheduler) {
        $task->setSendValue($task->getTaskId());
        $scheduler->schedule($task);
    });
}

function newTask(Generator $coroutine) {
    return new SystemCall(
        function(Task $task, Scheduler $scheduler) use ($coroutine) {
            $task->setSendValue($scheduler->newTask($coroutine));
            $scheduler->schedule($task);
        }
    );
}

function killTask($tid) {
    return new SystemCall(
        function(Task $task, Scheduler $scheduler) use ($tid) {
            $task->setSendValue($scheduler->killTask($tid));
            $scheduler->schedule($task);
        }
    );
}

/*function task($max) {
    $tid = (yield getTaskId()); // <-- here's the syscall!
    for ($i = 1; $i <= $max; ++$i) {
        echo "This is task $tid iteration $i.\n";
        yield;
    }
}

$scheduler = new Scheduler;

$scheduler->newTask(task(10));
$scheduler->newTask(task(5));

$scheduler->run();*/

function childTask() {
    $tid = (yield getTaskId());
    while (true) {
        echo "Child task $tid still alive!\n";
        yield;
    }
}

function task() {
    $tid = (yield getTaskId());
    $childTid = (yield newTask(childTask()));

    for ($i = 1; $i <= 6; ++$i) {
        echo "Parent task $tid iteration $i.\n";
        yield;

        if ($i == 3) yield killTask($childTid);
    }
}

$scheduler = new Scheduler;
$scheduler->newTask(task());
$scheduler->run();