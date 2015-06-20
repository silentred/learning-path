## 效果

```
输入 a，会自动提示 apple、application、acfun、adobe；
输入 ap，提示 apple、application；
输入 ac，提示 acfun；
输入 ad，提示 adobe。
```

## redis的sorted set(有序数组)
```
ZADD word:a 0 apple 0 application 0 acfun 0 adobe
ZADD word:ap 0 apple 0 application
ZADD word:app 0 apple 0 application
ZADD word:appl 0 apple 0 application
ZADD word:apple 0 apple
ZADD word:appli 0 application
```
这里的分数都是0，把分数统一设置到word_scores集合中

## 加入排序热度
```
ZADD word_scores 100 apple 80 adobe 70 application 60 acfun
```
需要更新时，可以只更新word_result中的分数

## 取交集
```
ZINTERSTORE word_result 2 word_scores word:a WEIGHTS 1 1 #取交集，把分数相加。
ZREVRANGE word_result 0 -1 withscores #倒序取集合
```

## php代码
```php
<?php

namespace Blog\Redis;

use \Redis;


class Suggest {

    const PREFIX = 'word:';
    const WORDS_PREFIX = 'word_scores';
    const RESULT_PREFIX = 'word_result';

    protected $redis = null;


    public function __construct(Redis $redis) {
        $this->redis = $redis;
    }


    public function add($word) {
        $len = mb_strlen($word, 'UTF-8');
        for ($i = 1; $i <= $len; $i++) {
            $sub = mb_substr($word, 0, $i, 'UTF-8');
            $this->redis->zAdd(self::PREFIX . $sub, 0, $word);
        }
    }


    public function incScore($word, $score = 1) {
        return $this->redis->zIncrBy(self::WORDS_PREFIX, $score, $word);
    }


    public function search($keyword, $stop = 5) {
        $this->redis->zInter(self::RESULT_PREFIX, array(self::PREFIX . $keyword, self::WORDS_PREFIX), array(1, 1));
        return $this->redis->zRevRange(self::RESULT_PREFIX, 0, $stop, true);
    }

}
```
