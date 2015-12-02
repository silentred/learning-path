# 事件广播

## 简介
Laravel 5.1 之中新加入了事件广播的功能，作用是把服务器中触发的事件通过websocket服务通知客户端，也就是浏览器，客户端js根据接受到的事件，做出相应动作。本文会用简单的代码展示一个事件广播的过程。

## 依赖
- redis
- nodejs, socket.io
- laravel 5.1

## 配置
`config/broadcasting.php`中，如下配置`'default' => env('BROADCAST_DRIVER', 'redis'),`，使用redis作为php和js的通信方式。
`config/database.php`中配置redis的连接。

## 定义一个被广播的事件
根据Laravel文档的说明，想让事件被广播，必须让`Event`类实现一个`Illuminate\Contracts\Broadcasting\ShouldBroadcast`接口，并且实现一个方法`broadcastOn`。`broadcastOn`返回一个数组，包含了事件发送到的`channel`(频道)。如下：

    namespace App\Events;
    
    use App\Events\Event;
    use Illuminate\Queue\SerializesModels;
    use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
    
    class SomeEvent extends Event implements ShouldBroadcast
    {
        use SerializesModels;
    
        public $user_id;
    
        /**
         * Create a new event instance.
         *
         * @return void
         */
        public function __construct($user_id)
        {
            $this->user_id = $user_id;
        }
    
        /**
         * Get the channels the event should be broadcast on.
         *
         * @return array
         */
        public function broadcastOn()
        {
            return ['test-channel'];
        }
    }
    
## 被广播的数据
默认情况下，`Event`中的所有public属性都会被序列化后广播。上面的例子中就是`$user_id`这个属性。你也可以使用`broadcastWith`这个方法，明确的指出要广播什么数据。例如：

    public function broadcastWith()
    {
        return ['user_id' => $this->user_id];
    }

## Redis和Websocket服务器
- 需要启动一个Redis，事件广播主要依赖的就是redis的sub/pub功能，具体可以看redis文档

- 需要启动一个websocket服务器来和client通信，建议使用socket.io，代码如下:

        var app = require('http').createServer(handler);
        var io = require('socket.io')(app);
        
        var Redis = require('ioredis');
        var redis = new Redis('6379', '192.168.1.106');
        
        app.listen(6001, function() {
            console.log('Server is running!');
        });
        
        function handler(req, res) {
            res.writeHead(200);
            res.end('');
        }
        
        io.on('connection', function(socket) {
            console.log('connected');
        });
        
        redis.psubscribe('*', function(err, count) {
            console.log(count);
        });
        
        redis.on('pmessage', function(subscribed, channel, message) {
            console.log(subscribed);
            console.log(channel);
            console.log(message);
        
            message = JSON.parse(message);
            io.emit(channel + ':' + message.event, message.data);
        });
    
这里需要注意的是`redis.on`方法的定义,接收到消息后，给client发送一个事件，事件名称为`channel + ':' + message.event`。

## 客户端代码
客户端我们也使用socket.io，作为测试，代码尽量简化，仅仅打印一个接受到的数据即可。如下：

    var socket = io('http://localhost:6001');
    socket.on('connection', function (data) {
        console.log(data);
    });
    socket.on('test-channel:App\\Events\\SomeEvent', function(message){
        console.log(message);
    });
    console.log(socket);
    
## 服务器触发事件
直接在router中定义个事件触发即可。如下：

    Route::get('/event', function(){
        Event::fire(new \App\Events\SomeEvent(3));
        return "hello world";
    });
    
## 测试
- 启动redis
- 启动websocket
- 打开带有客户端代码的页面，可以看到websocket已经连接成功。
- 触发事件,打开另一个页面 `localhost/event`。

这时就可以发现，第一个页面的console中打印出了`Object{user_id: 3}`，说明广播成功。

我录了一个[教学视频](http://v.youku.com/v_show/id_XMTI2MzMwMTIzMg==.html)，大家如有不明白可以参考这个视频。
































> 因为最近在学习Go，所以找了revel这个框架来学习，感觉和php的面向对象有很大不同。revel没有提供db mapping的组件，所以在github上搜了很多ORM来学习，在`jmoiron/sqlx`中发现了一篇比较详细介绍`database/sql`这个包的文章，拿来和大家分享。本文并不是按字句的翻译，如果哪里表述不清楚建议阅读原文 [原文地址](http://go-database-sql.org/index.html)

## 概述

`sql.DB`不是一个连接，它是数据库的抽象接口。它可以根据driver打开关闭数据库连接，管理连接池。正在使用的连接被标记为繁忙，用完后回到连接池等待下次使用。所以，如果你没有把连接释放回连接池，会导致过多连接使系统资源耗尽。

## 使用DB

### 导入driver
这里使用的是[MySQL drivers](https://github.com/go-sql-driver/mysql)
```
import (
	"database/sql"
	_ "github.com/go-sql-driver/mysql"
)
```

### 连接DB

```
func main() {
	db, err := sql.Open("mysql",
		"user:password@tcp(127.0.0.1:3306)/hello")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
}
```

`sql.Open`的第一个参数是driver名称，第二个参数是driver连接数据库的信息，各个driver可能不同。DB不是连接，并且只有当需要使用时才会创建连接，如果想立即验证连接，需要用`Ping()`方法，如下：
```
err = db.Ping()
if err != nil {
	// do something here
}
```
sql.DB的设计就是用来作为长连接使用的。不要频繁Open, Close。比较好的做法是，为每个不同的datastore建一个DB对象，保持这些对象Open。如果需要短连接，那么把DB作为参数传入function，而不要在function中Open, Close。

### 读取DB
如果方法包含`Query`，那么这个方法是用于查询并返回rows的。其他情况应该用`Exec()`。
```
var (
	id int
	name string
)
rows, err := db.Query("select id, name from users where id = ?", 1)
if err != nil {
	log.Fatal(err)
}
defer rows.Close()
for rows.Next() {
	err := rows.Scan(&id, &name)
	if err != nil {
		log.Fatal(err)
	}
	log.Println(id, name)
}
err = rows.Err()
if err != nil {
	log.Fatal(err)
}
```

上面代码的过程为：`db.Query()`表示向数据库发送一个query，`defer rows.Close()`非常重要，遍历rows使用`rows.Next()`， 把遍历到的数据存入变量使用`rows.Scan()`, 遍历完成后检查error。有几点需要注意：

1. 检查遍历是否有error
2. 结果集(rows)未关闭前，底层的连接处于繁忙状态。当遍历读到最后一条记录时，会发生一个内部EOF错误，自动调用`rows.Close()`，但是如果提前退出循环，rows不会关闭，连接不会回到连接池中，连接也不会关闭。所以手动关闭非常重要。`rows.Close()`可以多次调用，是无害操作。

### 单行Query

err在`Scan`后才产生，所以可以如下写：
```
var name string
err = db.QueryRow("select name from users where id = ?", 1).Scan(&name)
if err != nil {
	log.Fatal(err)
}
fmt.Println(name)
```

## 修改数据，事务

一般用Prepared Statements和`Exec()`完成`INSERT`, `UPDATE`, `DELETE`操作。
```
stmt, err := db.Prepare("INSERT INTO users(name) VALUES(?)")
if err != nil {
	log.Fatal(err)
}
res, err := stmt.Exec("Dolly")
if err != nil {
	log.Fatal(err)
}
lastId, err := res.LastInsertId()
if err != nil {
	log.Fatal(err)
}
rowCnt, err := res.RowsAffected()
if err != nil {
	log.Fatal(err)
}
log.Printf("ID = %d, affected = %d\n", lastId, rowCnt)
```

### 事务

`db.Begin()`开始事务，`Commit()` 或 `Rollback()`关闭事务。`Tx`从连接池中取出一个连接，在关闭之前都是使用这个连接。Tx不能和DB层的`BEGIN`, `COMMIT`混合使用。

如果你需要通过多条语句修改连接状态，你必须使用Tx，例如：

- 创建仅对单个连接可见的临时表
- 设置变量，例如`SET @var := somevalue`
- 改变连接选项，例如字符集，超时


## Prepared Statements

### Prepared Statements and Connection

在数据库层面，Prepared Statements是和单个数据库连接绑定的。客户端发送一个有占位符的statement到服务端，服务器返回一个statement ID，然后客户端发送ID和参数来执行statement。

在GO中，连接不直接暴露，你不能为连接绑定statement，而是只能为DB或Tx绑定。`database/sql`包有自动重试等功能。当你生成一个Prepared Statement

1. 自动在连接池中绑定到一个空闲连接
2. `Stmt`对象记住绑定了哪个连接
3. 执行`Stmt`时，尝试使用该连接。如果不可用，例如连接被关闭或繁忙中，会自动re-prepare，绑定到另一个连接。

这就导致在高并发的场景，过度使用statement可能导致statement泄漏，statement持续重复prepare和re-prepare的过程，甚至会达到服务器端statement数量上限。

某些操作使用了PS，例如`db.Query(sql, param1, param2)`, 并在最后自动关闭statement。

有些场景不适合用statement：

1. 数据库不支持。例如Sphinx，MemSQL。他们支持MySQL wire protocol, 但不支持"binary" protocol。
2. statement不需要重用很多次，并且有其他方法保证安全。[例子](https://vividcortex.com/blog/2014/11/19/analyzing-prepared-statement-performance-with-vividcortex/)


### 在Transaction中使用PS

PS在Tx中唯一绑定一个连接，不会re-prepare。

Tx和statement不能分离，在DB中创建的statement也不能在Tx中使用，因为他们必定不是使用同一个连接使用Tx必须十分小心，例如下面的代码：
```
tx, err := db.Begin()
if err != nil {
	log.Fatal(err)
}
defer tx.Rollback()
stmt, err := tx.Prepare("INSERT INTO foo VALUES (?)")
if err != nil {
	log.Fatal(err)
}
defer stmt.Close() // danger!
for i := 0; i < 10; i++ {
	_, err = stmt.Exec(i)
	if err != nil {
		log.Fatal(err)
	}
}
err = tx.Commit()
if err != nil {
	log.Fatal(err)
}
// stmt.Close() runs here!
```
`*sql.Tx`一旦释放，连接就回到连接池中，这里stmt在关闭时就无法找到连接。所以必须在Tx commit或rollback之前关闭statement。


## 处理Error

### 循环Rows的Error
如果循环中发生错误会自动运行`rows.Close()`，用`rows.Err()`接收这个错误，Close方法可以多次调用。循环之后判断error是非常必要的。
```
for rows.Next() {
	// ...
}
if err = rows.Err(); err != nil {
	// handle the error here
}
```

### 关闭Resultsets时的error
如果你在rows遍历结束之前退出循环，必须手动关闭Resultset，并且接收error。
```
for rows.Next() {
	// ...
	break; // whoops, rows is not closed! memory leak...
}
// do the usual "if err = rows.Err()" [omitted here]...
// it's always safe to [re?]close here:
if err = rows.Close(); err != nil {
	// but what should we do if there's an error?
	log.Println(err)
}
```

### QueryRow()的error

```
var name string
err = db.QueryRow("select name from users where id = ?", 1).Scan(&name)
if err != nil {
	log.Fatal(err)
}
fmt.Println(name)
```
如果id为1的不存在，err为sql.ErrNoRows，一般应用中不存在的情况都需要单独处理。此外，Query返回的错误都会延迟到Scan被调用，所以应该写成如下代码：
```
var name string
err = db.QueryRow("select name from users where id = ?", 1).Scan(&name)
if err != nil {
	if err == sql.ErrNoRows {
		// there were no rows, but otherwise no error occurred
	} else {
		log.Fatal(err)
	}
}
fmt.Println(name)
```
把空结果当做Error处理是为了强行让程序员处理结果为空的情况


### 分析数据库Error

各个数据库处理方式不太一样，mysql为例：
```
if driverErr, ok := err.(*mysql.MySQLError); ok { 
	// Now the error number is accessible directly
	if driverErr.Number == 1045 {
		// Handle the permission-denied error
	}
}
```
`MySQLError`, `Number`都是DB特异的，别的数据库可能是别的类型或字段。这里的数字可以替换为常量，例如这个包 [MySQL error numbers maintained by VividCortex](https://github.com/VividCortex/mysqlerr)

### 连接错误

## NULL值处理

简单说就是设计数据库的时候不要出现null，处理起来非常费力。Null的type很有限，例如没有`sql.NullUint64`; null值没有默认零值。
```
for rows.Next() {
	var s sql.NullString
	err := rows.Scan(&s)
	// check err
	if s.Valid {
	   // use s.String
	} else {
	   // NULL value
	}
}
```

## 未知Column

`rows.Columns()`的使用，用于处理不能得知结果字段个数或类型的情况，例如：
```
cols, err := rows.Columns()
if err != nil {
	// handle the error
} else {
	dest := []interface{}{ // Standard MySQL columns
		new(uint64), // id
		new(string), // host
		new(string), // user
		new(string), // db
		new(string), // command
		new(uint32), // time
		new(string), // state
		new(string), // info
	}
	if len(cols) == 11 {
		// Percona Server
	} else if len(cols) > 8 {
		// Handle this case
	}
	err = rows.Scan(dest...)
	// Work with the values in dest
}
```

```
cols, err := rows.Columns() // Remember to check err afterwards
vals := make([]interface{}, len(cols))
for i, _ := range cols {
	vals[i] = new(sql.RawBytes)
}
for rows.Next() {
	err = rows.Scan(vals...)
	// Now you can check each element of vals for nil-ness,
	// and you can use type introspection and type assertions
	// to fetch the column into a typed variable.
}
```

## 关于连接池

1. 避免错误操作，例如LOCK TABLE后用 INSERT会死锁，因为两个操作不是同一个连接，insert的连接没有table lock。
2. 当需要连接，且连接池中没有可用连接时，新的连接就会被创建。
3. 默认没有连接上限，你可以设置一个，但这可能会导致数据库产生错误“too many connections”
4. `db.SetMaxIdleConns(N)`设置最大空闲连接数
5. `db.SetMaxOpenConns(N)`设置最大打开连接数
6. 长时间保持空闲连接可能会导致db timeout


























> 服务端的开发离不开协议，swoole的出现对于学习通信来说，无疑是非常好的教材。非常推荐大家下载 [Swoole Framework](https://github.com/swoole/framework)，其中包含了多种协议的php实现，例如FTP，HTTP，Websocket等。本文大部分代码都是受这个项目的启发，当然学习的同时别忘了star一下这个项目。笔者本身计算机基础较弱，写这篇文章的同时也查了不少资料，如果有错误欢迎提出批评。

## websocket协议学习

### 概述
协议分为两部分：握手，数据传输

客户端发出的握手信息类似：

```
GET /chat HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Origin: http://example.com
Sec-WebSocket-Protocol: chat, superchat
Sec-WebSocket-Version: 13
```

服务器返回的握手信息类似：

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
Sec-WebSocket-Protocol: chat
Sec-WebSocket-Version: 13
```

两段信息的第一行大家应该都比较熟悉，是HTTP协议中的Request-Line和Status-Line，[RFC2616](https://tools.ietf.org/html/rfc2616)。下面接着出现的是无序的头信息，这和HTTP协议相同。 一旦握手成功，一个双向连接通道就建立了。
连接用于传输`message`, `message`由一个或多个`frame`组成。每个frame有一个类型，属于同一个message的frame的类型都相同。类型包括：文本，二进制，control frame(协议层信号)等。目前一共有6种类型，10种保留类型。

### 握手

根据上面的客户端头信息可以看出，握手和HTTP是兼容的。WS的握手是HTTP的"升级版本"。

客户端发送的握手请求必须
1. 是一个合法的HTTP请求
2. 方法是GET
3. 头必须包含HOST字段
4. 头必须包含Upgrade字段，值为websocket,可以看作是判断请求为ws的标志。
5. 头必须包含Connection字段，值为Upgrade。
6. 头必须包含Sec-WebSocket-Key字段，用于验证。
7. 如果请求来自浏览器，头必须包含 Origin字段。
8. 头必须包含Sec-WebSocket-Version字段，值为13

### 验证握手

取`Sec-WebSocket-Key `字段的值，连接一个GUID字符串,"258EAFA5-E914-47DA-95CA-C5AB0DC85B11", sha1 hash一下，再base64_encode，得到的值作为字段`Sec-WebSocket-Accept`的值返回给客户端。用php代码表示:

```
'Sec-WebSocket-Accept' => base64_encode(sha1($key . static::GUID, true))
```

同时，返回的状态设置为101，其他状态都表示握手没有成功。 `Connection`,`Upgrade`字段作为HTTP升级版必须存在。一个握手返回如下：

```
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

### Frame(帧)的结构如下：
```
  0                   1                   2                   3
  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
 +-+-+-+-+-------+-+-------------+-------------------------------+
 |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
 |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
 |N|V|V|V|       |S|             |   (if payload len==126/127)   |
 | |1|2|3|       |K|             |                               |
 +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
 |     Extended payload length continued, if payload len == 127  |
 + - - - - - - - - - - - - - - - +-------------------------------+
 |                               |Masking-key, if MASK set to 1  |
 +-------------------------------+-------------------------------+
 | Masking-key (continued)       |          Payload Data         |
 +-------------------------------- - - - - - - - - - - - - - - - +
 :                     Payload Data continued ...                :
 + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
 |                     Payload Data continued ...                |
 +---------------------------------------------------------------+
```

- `FIN`: 1 bit, 标记是否是最后一个message的最后一个片段
- `RSV1`, `RSV2`, `RSV3`： 各 1 bit, 保留标记，都为0
- `Opcode`：4 bits， 是对payload data的说明，指明这个帧的类型。
1. 0x0 表明为接着上一帧的连续帧
2. 0x1 表明为text frame
3. 0x2 表明为binary frame
4. 0x3-7 保留
5. 0x8 表示连接关闭
6. 0x9 为ping
7. 0xA 为pong
8. 0xB-F 保留 
- `Mask`: 1 bit, 指明Payload data是否被mask，如果为1，那么数据需要根据masking-key来unmask。客户端发送的帧都是mask的。
- `Payload length`： 7 bits 或 7+16 bits 或 7+64 bits. 如果值为0-125，那么该值就是payload的长度；如果为126，那么接下来的2个byte表示payload长度(16bit, unsigned)； 如果为127，那么接下来的8个bytes表示payload的长度(64bit, unsigned)。
- `Masking-key`: 0 或 4 bytes, 用于unmask payload data。
- `Payload data`: 长度为 Payload length, 可以分为 extension data + application data, 扩展数据的长度计算方法是是事先商议好的，剩余的就是应用数据。
 
### Mask规则

`masking-key`是客户端随意指定的32bit长度值。从原始数据到masked数据的方式为：`原始数据第i个字节的值 XOR masking-key的第(i%4)个字节的值`。XOR表示异或，%表示取模。


### 片段化的作用

当传递一个未知长度的数据时，可以不用一下子buffer全部的数据。尤其当数据非常大时，可以分多次buffer，包装为frame来发送。

### 尝试解析一个frame

看到这里，我们已经了解了frame的结构，是否想尝试解析一个frame，官方文档提供了几段[二进制数据](https://tools.ietf.org/html/rfc6455#page-38)，我们可以用来练习一下。我挑选了其中两段, 代码如下：

```php
<?php

//A single-frame unmasked text message
$data = array(0x81, 0x05, 0x48, 0x65, 0x6c, 0x6c, 0x6f);
//A single-frame masked text message
$data2 = array(0x81, 0x85, 0x37, 0xfa, 0x21, 0x3d, 0x7f, 0x9f, 0x4d, 0x51, 0x58);


handleData(toString($data));
handleData(toString($data2));

function toString(array $data) {
    return array_reduce($data, function($carry, $item){
        return $carry .= chr($item);
    });
}

function handleData($data){
	$offset = 0;

	$temp = ord($data[$offset++]);
	$FIN = ($temp >> 7) & 0x1;
	$RSV1 = ($temp >> 6) & 0x1;
	$RSV2 = ($temp >> 5) & 0x1;
	$RSV3 = ($temp >> 4) & 0x1;
	$opcode = $temp & 0xf;

	echo "First byte: FIN is $FIN, RSV1-3 are $RSV1, $RSV2, $RSV3; Opcode is $opcode \n";

	$temp = ord($data[$offset++]);
	$mask = ($temp >> 7) & 0x1;
	$payload_length = $temp & 0x7f;
	if($payload_length == 126){
		$temp = substr($data, $offset, 2);
		$offset += 2;
		$temp = unpack('nl', $temp);
		$payload_length = $temp['l'];
	}elseif($payload_length == 127){
		$temp = substr($data, $offset, 8);
		$offset += 8;
		$temp = unpack('nl', $temp);
		$payload_length = $temp['l'];
	}
	echo "mask is $mask, payload_length is $payload_length \n";

	if($mask ==0){
		$temp = substr($data, $offset);
		$content = '';
        for ($i=0; $i < $payload_length; $i++) { 
            $content .= $temp[$i];
        }
	}else{
		$masking_key = substr($data, $offset, 4);
		$offset += 4;
		
		$temp = substr($data, $offset);
		$content = '';
        for ($i=0; $i < $payload_length; $i++) { 
            $content .= chr(ord($temp[$i]) ^ ord($masking_key[$i%4]));
        }
	}

	echo "content is $content \n";
}
```
结果输出如下图：

![output result][1]

> 到这里其实并不算完，ws协议还有很多很多规则，RFC文档实在是太长了。比如，如何应对每一种control frame，有详细的说明；如何关闭连接；协议扩展；错误处理；安全相关；一些基本的内容都能在swoole framework中找到对应的代码。


  [1]: /img/bVm1yL
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  > 最近需要用Instagram的api抓取其用户的图片，由于需要用oauth2验证, 所以应用必须包含一个web界面。设想能够实时返回下载数量，所以用websocket。还有需要考虑到效率问题，综合以上几点，想用一门语言开发的话，最终选择用golang进行开发，node的回调实在不喜欢。

## 前言

关于golang的web开发有不少框架，例如 martini, gin, revel，gorilla等。 之前玩过`revel`，感觉封装的太多了，作为一个小应用不需要这么复杂，而且google得到结果是revel的效率相对较差。`gin`的benchmark显示效率是martini的40倍，但是gin比较新所以他的的生态圈相对较少。最终选择了`martini`, 有很多middleware可以选择，其中就包括了websocket，并且背后用的是gorilla websocket这个包。

## 界面和功能

1. 一个跳转到Oauth2登陆授权页面的链接
2. 授权完成后，跳回服务的页面，此时获得了access_token, 就可以为所欲为了。全部的功能也都集中在这个页面，最终的界面如下图所示。

![界面和功能][1]


`点击连接`是用来打开websocket连接的。`开始发送数据`是开始把用户ID发给服务端，服务端调用api开始抓取图片。`停止`用于停止本次的抓取服务。`已完成数量`用于实时返回抓取的图片数量。


## 程序大致结构

![程序大致结构][2]

这里把`Jobs`, `goroutine #1`, `#2`等作用在全局是为了在websocket断开后，下载还能继续执行。`websocket goroutine`是连接建立后的作用域，连接断开后这个goroutine就不存在了。`Jobs`, `NextUrl`充当队列的角色。 `Done`的作用仅仅是计数。这里少写了两个全局变量，`Quit chan int`, `IsPreparing bool`, 这两个变量是用来让前端控制抓取程序是否进行的。

简单理解就是一个产生任务的for循环，一个消费任务的for循环，一个用于给client返回计数的for循环。这里不得不感叹，goroutine channel的设计使得编码简单明了。

## 遇到的问题
由于第一次正经使用Go，还是遇到不少问题的。不过需求比较简单，所以没有接触什么深入的内容。主要集中在强类型带来的问题。

### DB查询
之前写过一篇关于[database/sql](http://segmentfault.com/a/1190000003036452)的文章，这次直接用了`sqlx`这个库，可以少写不少代码，也少犯错误。但是毕竟不如laravel那么方便，所幸需要写的sql不多，临时写几个方法就搞定。同时思考，如何实现一个eloquent的api。貌似有难度。

### Json处理
强类型决定了Json的处理是个痛。之前写过一个天气预报的小程序，用的是`map[string]*json.RawMessage` 这种映射结构，然后一层一层解开json。当时没发现这是有问题的，因为如果用`RawMessage`, 字符串的引号`"`也会被保留，使得字符串结果前后多了引号。
这次再次google了一次，发现还是得用`map[string]interface{}`来映射，然后再用`type assertion`来一层层的解开json。这是一个痛苦的过程，想起php中的`json_decode()`不禁泪流满面。

### Stop Goroutine
如何中断一个goroutine是一个问题，因为需要控制开始停止。谷歌一下很快就有结果。
```golang
    go func() {
		for {
			select {
			case <-Quit:
				IsPreparingJobs = false
				return
			default:
			    // to do something
			}

		}
	}()
```
这里设置一个`IsPreparingJobs`是用于中断后再次开始这个循环。

### Testing
Golang提供的测试工具非常方便，`go test`就能进行所有测试。从martini源码中复制了两个常用方法出来。
```golang
func expect(t *testing.T, a interface{}, b interface{}) {
	if a != b {
		t.Errorf("Expected %v (type %v) - Got %v (type %v)", b, reflect.TypeOf(b), a, reflect.TypeOf(a))
	}
}

func refute(t *testing.T, a interface{}, b interface{}) {
	if a == b {
		t.Errorf("Did not expect %v (type %v) - Got %v (type %v)", b, reflect.TypeOf(b), a, reflect.TypeOf(a))
	}
}
```

## 总结
感觉golang作为web开发工具，在数据格式处理方面，没有弱类型语言方便。这点node倒是非常好，json转object非常方便。也许配合Promise，node会比较好用吧。golang也有优势，goroutine非常好用，官方的库功能非常全，打包为二进制可执行文件使得部署异常容易，强类型语言效率比较高。

最后有感于前几天的shadowsockets事件，作为一个ss使用者，除了感谢无私的开发者，剩下的就只是愤怒和失望。昨天又看了老罗的T1发布会，`Born to be proud`, `天生骄傲`，在坚持做人原则方面，老罗一直是我的楷模。期待今晚的锤子发布会。


  [1]: /img/bVoOko
  [2]: /img/bVoOas
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  > Laravel5实现用户友好的错误页面非常简单，例如想要返回status 404，只需要在`view/errors`中添加一个`404.blade.php`文件即可。Lumen中没有默认实现这种便利，于是自己添加一个。

# Lumen如何实现类Laravel5用户友好的错误页面

## 原理

抛出错误的函数是`abort()`, 进入该函数一看究竟，会发现只是抛出一个`HttpException`. 在Application中，处理http request的时候，有一个try catch的过程，Exception就是在这里被捕获的。

```php
try {
    return $this->sendThroughPipeline($this->middleware, function () use ($method, $pathInfo) {
        if (isset($this->routes[$method.$pathInfo])) {
            return $this->handleFoundRoute([true, $this->routes[$method.$pathInfo]['action'], []]);
        }

        return $this->handleDispatcherResponse(
            $this->createDispatcher()->dispatch($method, $pathInfo)
        );
    });
} catch (Exception $e) {
    return $this->sendExceptionToHandler($e);
}
```

接着可以看出，Exception是交给了`sendExceptionToHandler`去处理了。这里的handler具体是哪个类呢？是实现了`Illuminate\Contracts\Debug\ExceptionHandler`的一个单例。为啥说他是单例？因为在bootstrap的时候，已经初始化为单例了，请看。

```php
$app->singleton(
    Illuminate\Contracts\Debug\ExceptionHandler::class,
    App\Exceptions\Handler::class
);
```

进入该类看一下，他有一个`render`方法，好吧，找到问题所在了，修改一下这个方法即可。

```php
public function render($request, Exception $e)
{
    return parent::render($request, $e);
}
```

## 动手修改

由于Laravel已经有实现了，所以最简便的方法就是复制黏贴。在`render`中先判断下是否为`HttpException`, 如果是，就去`errors`目录下找对应status code的view，如果找到，就渲染它输出。就这么简单。修改`Handler`如下：

```php
/**
 * Render an exception into an HTTP response.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  \Exception  $e
 * @return \Illuminate\Http\Response
 */
public function render($request, Exception $e)
{
    if( !env('APP_DEBUG') and $this->isHttpException($e)) {
        return $this->renderHttpException($e);
    }
    return parent::render($request, $e);
}

/**
 * Render the given HttpException.
 *
 * @param  \Symfony\Component\HttpKernel\Exception\HttpException  $e
 * @return \Symfony\Component\HttpFoundation\Response
 */
protected function renderHttpException(HttpException $e)
{
    $status = $e->getStatusCode();

    if (view()->exists("errors.{$status}"))
    {
        return response(view("errors.{$status}", []), $status);
    }
    else
    {
        return (new SymfonyExceptionHandler(env('APP_DEBUG', false)))->createResponse($e);
    }
}

/**
 * Determine if the given exception is an HTTP exception.
 *
 * @param  \Exception  $e
 * @return bool
 */
protected function isHttpException(Exception $e)
{
    return $e instanceof HttpException;
}
```

好了，在`errors`目录下新建一个`404.blade.php`文件，在controller中尝试 `abort(404)`看一下吧。