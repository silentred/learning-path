<?php
/**
 * Created by PhpStorm.
 * User: Jason
 * Date: 11/22/2015
 * Time: 12:09 AM
 */

namespace App;


class SystemCall
{
    protected $callback;

    public function __construct(callable $callback) {
        $this->callback = $callback;
    }

    public function __invoke(Task $task, Scheduler $scheduler) {
        $callback = $this->callback; // Can't call it directly in PHP :/
        return $callback($task, $scheduler);
    }

}