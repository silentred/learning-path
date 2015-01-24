<?php
$connection = new MongoClient(); 
$db = $connection->test;
#print_r($db);

$users = $db->users;
#print_r($users);

$doc = [
	'name'=>'Eric',
	'age' => 30,
	'lang' => 'Java'
];
#print_r($users->insert($doc));

$user = $users->findOne();
#var_dump($user);

/*for ( $i = 0; $i < 3; $i++ )
{
    $users->insert( array( 'i' => $i, "field{$i}" => $i * 2 ) );
}*/

$count = $users->count();
var_dump($count);

/*$cursor = $users->find();
foreach($cursor as $id => $value){
	echo "$id: ";
	var_dump($value);
}*/

$query = array( 'name' => 'Eric' );
$cursor = $users->find($query);

$query = array( "i" => array( '$gt' => 0 ) );
$cursor = $users->find($query);

/*while( $cursor->hasNext()){
	var_dump($cursor->getNext());
}*/