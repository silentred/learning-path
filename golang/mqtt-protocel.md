# MQTT 协议学习笔记

## 格式

固定头, 共2个byte
Byte 1: Message Type (4), DUP (1), QoS level (2), and RETAIN  (1)
Byte 2: Remaining Length (at least one byte)

### Message Type

```
Mnemonic	Enumeration	Description

Reserved	0	Reserved
CONNECT 	1	Client request to connect to Server
CONNACK		2	Connect Acknowledgment
PUBLISH		3	Publish message
PUBACK		4	Publish Acknowledgment
PUBREC		5	Publish Received (assured delivery part 1)
PUBREL		6	Publish Release (assured delivery part 2)
PUBCOMP		7	Publish Complete (assured delivery part 3)
SUBSCRIBE	8	Client Subscribe request
SUBACK		9	Subscribe Acknowledgment
UNSUBSCRIBE	10	Client Unsubscribe request
UNSUBACK	11	Unsubscribe Acknowledgment
PINGREQ		12	PING Request
PINGRESP	13	PING Response
DISCONNECT	14	Client is Disconnecting
Reserved	15	Reserved
```

### Flags:

DUP:	Duplicate delivery, 重复传输

QoS:	Quality of Service 服务质量

RETAIN:	RETAIN flag 保留消息

#### DUP： 

当客户端或服务器重新传输 PUBLISH, PUBREL, SUBSCRIBE or UNSUBSCRIBE 消息时，需要设置这个值。
当QoS大于0时，需要 acknowledgement时，也适用。这个值设定就代表在 variable header中包含了 messageId.
该值若设定，接受者可以认为这个消息可能之前已经收到过，但是并不能作为绝对的依据。

#### QoS: PUBLISH的传输质量

QoS value	Description
0			At most once	Fire and Forget	<=1, 最多一次，客户的publish后就不管服务器有没有正确执行
1			At least once	Acknowledged delivery	>=1，最少一次，publish之后需要服务器回一个ACK
2			Exactly once	Assured delivery	=1，保证一次, msg type 中 5-7和这个模式相关
3			Reserved

#### RETAIN:
设为1时，服务器接受到PUBLISH，传递给当前订阅者后并不立刻销毁，而是保存。当新的订阅者订阅某个topic时，那个topic上最新的被保留的message被发送给新的订阅者。

When a server sends a PUBLISH to a client as a result of a subscription that already existed when the original PUBLISH arrived, the Retain flag should not be set, regardless of the Retain flag of the original PUBLISH. This allows a client to distinguish messages that are being received because they were retained and those that are being received "live".
这段部分没看懂，慢慢体会

restained messages应该在服务器重启后依旧存在（应该，有没有实现不清楚）

服务器何时删除retained message: 当服务器收到 某个topic上，0长payload, 并且设置了retain为1的消息时

*第一字节到此结束*

### Remaining Length:

剩余消息的字节数，包括了 `variable header`, `payload`。
第一个字节最高位的bit为标记位，如果为1，则代表长度超过了127，需要再加一个byte来表示；第二个字节
的最高位也是标记位，作用一致。所以，两个字节能够表示的最大长度是 2的14次方 - 1, （每个字节减去一个
标记bit，所以是14次方），也就是16383.

协议限制Remaining Length最多是 4个bytes，也就是下表所示的 268435455 byte, 256 MB.

这里看上去 Remaining Length 所占字节是可变的，但他并不是 variable header的一部分，所以
Remaining Length 所表示的长度，并不包含自身所占字节。

```
Digits	From	    To
1	      0 (0x00)	127 (0x7F)
2	      128 (0x80, 0x01)	16 383 (0xFF, 0x7F)
3	      16 384 (0x80, 0x80, 0x01)	2 097 151 (0xFF, 0xFF, 0x7F)
4	      2 097 152 (0x80, 0x80, 0x80, 0x01)	268 435 455 (0xFF, 0xFF, 0xFF, 0x7F)
```

官方文档中给出了算法，从数字到字符串，从字符串到数字，下面是PHP版本。

```
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

```

### 可变头 Variable Header

- Protocol Name: 
存在于 CONNECT, UTF编码的协议名称 "MQIsdp"

- Protocol Version:
8-bit unsigned value

- Connect Flags: 
1 byte, 包含以下flag `Clean Session`, `Will`, `Will Qos`, `Retain Flag` 在CONNECT消息中出现。

#### Clean Session
index为1的bit，index为0的bit是保留位。

为1时，当client断开连接，服务器丢弃所有关于这个client的状态。
为0时，当client断开，服务器保存该client的订阅信息，包括继续保存 相应topic的 Qos1, Qos2 消息；当client重新连接时，
client可以接受到这些消息。

#### Will flag
index为2的bit

当服务端IO错误或client没有在Keep Alive时间范围内响应，这个标志表示server代表client发送的消息。服务器收到 DISCONNECT 并不会触发这个message。

如果Will 被设定，那么 Will QoS, Will Retain也必须存在于 Connect Flags，并且 Will Topic, Will Message也必须存在于 payload

#### Will QoS
这个标志是针对 Will Message 的 QoS level，当client非自主（意外）断开时, Will Message 会被赋予这个 QoS级别来处理。 Will Message 存在于 CONNECT 的 payload

Will flag 必须设置，否则 Will QoS 被无视。

#### 








