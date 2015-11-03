<?php

// wait.php
$event = new SyncEvent("Test");
$event->wait();
echo "waiting is over. \n";

// fire.php
$event = new SyncEvent("Test");
$event->fire();
