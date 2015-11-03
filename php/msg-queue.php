<?php
// send-msg.php
// Here is an example of working with message queues.
$key_t = msg_get_queue(ftok("/tmp", 'R'));

// place two messages on the queue
if (!msg_send ($key_t, 1, 'This is message #1', true, true, $msg_err))
	echo "Msg not sent because $msg_err\n";
if (!msg_send ($key_t, 1, 'This is message #2 ', true, true, $msg_err))
	echo "Msg not sent because $msg_err\n";

// lets look at the queue structure 'msg_qnum' is really what we want to see
// it should be '2'
print_r(msg_stat_queue($key_t));

// get rid of the queue
//msg_remove_queue ($key_t);
sleep(1000);


// recieve-msg.php
if (msg_receive ($key_t, 1, $msg_type, 16384, $msg, true, 0, $msg_error)) {
   echo "$msg\n"; // prints 'This is message #1'
} else {
   echo "Received $msg_error fetching message\n";
}
// look at the structure again, ms_qnum should be '1'
print_r(msg_stat_queue($key_t));
if (msg_receive ($key_t, 2, $msg_type, 16384, $msg, true, 0, $msg_error)) {
   echo "$msg\n"; // prints 'This is message #2'
} else {
   echo "Received $msg_error fetching message\n";
}
// look at the structure again, ms_qnum should be '0', no more messages on the queue
print_r(msg_stat_queue($key_t));

