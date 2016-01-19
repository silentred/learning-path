<?php

use MongoDB\Driver\Manager;
use MongoDB\Driver\Query;
use MongoDB\Driver\Command;


$dsn = "mongodb://localhost:27017/users";
$options = [
'username' => 'admin',
'password' => 'public'
];

$manager = new Manager($dsn, $options);
$query = new Query(['city' => '北京市'], ['limit'=>5]);

$count = [
	'count' => 'usergeo',
	'query' => ['city'=>'北京市']
];

$aggregate = [
	'aggregate' => 'usergeo',
	'pipeline' => [
		['$match' => ['city'=>'北京市']],
		['$group' => ['_id'=>null, 'avg_time'=>['$avg'=>'$created_at']]]
	]
];

try {
    /* Specify the full namespace as the first argument, followed by the query
     * object and an optional read preference. MongoDB\Driver\Cursor is returned
     * success; otherwise, an exception is thrown. */
    $cursor = $manager->executeQuery("users.usergeo", $query);

    // Iterate over all matched documents
    $array = iterator_to_array($cursor);

    foreach ($array as $key => $value) {
    	$value = (array) $value;
    	var_dump($value['city']);
    	var_dump($value['province']);
    }

// count command
    $command = new Command($count);
    $result   = $manager->executeCommand("users", $command);
    $response = $result->toArray();
    var_dump($response);

// aggregate
    $command = new Command($aggregate);
    $result   = $manager->executeCommand("users", $command);
    $response = $result->toArray();
    var_dump($response);


} catch (MongoDB\Driver\Exception\Exception $e) {
    echo $e->getMessage(), "\n";
}
