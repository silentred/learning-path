<?php
class Iter implements Iterator{
    //Traversable 代表此类可以被foreach。Traversable无法实现。
    public $attributes;

    public function  __construct($attributes=array()){
        $this->attributes = $attributes;
    }

    public function current()
    {
        return current($this->attributes);
    }

    public function next()
    {
        return next($this->attributes);
    }

    public function key()
    {
        return key($this->attributes);
    }

    public function valid()
    {
        return key($this->attributes) !== null;
    }

    public function rewind()
    {
        return reset($this->attributes);
    }
}

$a = array(
    'id'=>12,
    'name' => 'Jason',
    'email' => 'silentred@163.com'
);
$iter = new Iter($a);
foreach($iter as  $key=>$value){
    echo "key is $key, value is $value \n";
}

class Iter2 implements IteratorAggregate{

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Retrieve an external iterator
     * @link http://php.net/manual/en/iteratoraggregate.getiterator.php
     * @return Traversable An instance of an object implementing <b>Iterator</b> or
     * <b>Traversable</b>
     */
    public function getIterator()
    {
        // TODO: Implement getIterator() method.返回一个迭代器，类似上面的 Iter 类，或者ArrayIterator等
    }

}

class Arr implements ArrayAccess{

    public $attr;

    public function __construct($attr){
        $this->attr = $attr;
    }
    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Whether a offset exists
     * @link http://php.net/manual/en/arrayaccess.offsetexists.php
     * @param mixed $offset <p>
     * An offset to check for.
     * </p>
     * @return boolean true on success or false on failure.
     * </p>
     * <p>
     * The return value will be casted to boolean if non-boolean was returned.
     */
    public function offsetExists($offset)
    {
        return array_key_exists($offset, $this->attr);
    }

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Offset to retrieve
     * @link http://php.net/manual/en/arrayaccess.offsetget.php
     * @param mixed $offset <p>
     * The offset to retrieve.
     * </p>
     * @return mixed Can return all value types.
     */
    public function offsetGet($offset)
    {
        return $this->attr[$offset];
    }

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Offset to set
     * @link http://php.net/manual/en/arrayaccess.offsetset.php
     * @param mixed $offset <p>
     * The offset to assign the value to.
     * </p>
     * @param mixed $value <p>
     * The value to set.
     * </p>
     * @return void
     */
    public function offsetSet($offset, $value)
    {
        if (is_null($offset)) {
            $this->attr[] = $value;
        } else {
            $this->attr[$offset] = $value;
        }
    }

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Offset to unset
     * @link http://php.net/manual/en/arrayaccess.offsetunset.php
     * @param mixed $offset <p>
     * The offset to unset.
     * </p>
     * @return void
     */
    public function offsetUnset($offset)
    {
        unset($this->attr[$offset]);
    }
}

$arr = new Arr(array('a'=>'AAA', 'b'=>'bbb'));
echo $arr['a']. "\n";
echo $arr['b']. "\n";
//echo $arr['c']. "\n"; //报错 undefined index
unset($arr["two"]);
var_dump(isset($arr["two"]));
$arr["two"] = "A value";
var_dump($arr["two"]);
$arr[] = 'Append 1';
print_r($arr);

echo time() - strtotime('2015-12-16 19:30:40');
echo "\n";

// MQTT payload length

$x = 321; // 65 + 128*2
$x = 449; // 65 + 128*3
$x = 16384;

function numToDigit($x){
    $return = '';
    do {
        $digit = $x % 128;
        $x = floor($x / 128);
        if ($x > 0) {
            $digit = $digit | 0x80;
        }
        $return .= chr($digit);
    }while ( $x > 0);

    return $return;
}

var_dump(numToDigit(321));

function digitToNum($string='')
{
    $multiplier = 1;
    $value = 0;
    $offset = 0;
    $length = strlen($string);
    //var_dump($length);
    do {
        $digit = ord($string[$offset++]);
        $value += ($digit & 127) * $multiplier;
        $multiplier *= 128;
    } while ( $offset <= $length && ($digit & 128)!=0 );

    return $value;
}

var_dump( digitToNum(numToDigit(321)) );


