# MQTT 协议学习笔记

## 格式

固定头, 共2个byte
Byte 1: Message Type (4), DUP (1), QoS level (2), and RETAIN  (1)
Byte 2: Remaining Length (at least one byte)

#### Message Type

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

Flags:

DUP:	Duplicate delivery, 重复传输

QoS:	Quality of Service 服务质量

RETAIN:	RETAIN flag 保留消息

- DUP： 当客户端或服务器重新传输 PUBLISH, PUBREL, SUBSCRIBE or UNSUBSCRIBE 消息时，需要设置这个值。
当QoS大于0时，需要 acknowledgement时，也适用。这个值设定就代表在 variable header中包含了 messageId.
该值若设定，接受者可以认为这个消息可能之前已经收到过，但是并不能作为绝对的依据。

- QoS: PUBLISH的传输质量

QoS value	Description
0			At most once	Fire and Forget	<=1, 最多一次，客户的publish后就不管服务器有没有正确执行
1			At least once	Acknowledged delivery	>=1，最少一次，publish之后需要服务器回一个ACK
2			Exactly once	Assured delivery	=1，保证一次, msg type 中 5-7和这个模式相关
3			Reserved

- RETAIN:
设为1时，服务器接受到PUBLISH，传递给当前订阅者后并不立刻销毁，而是保存。当新的订阅者订阅某个topic时，那个topic上最新的被保留的message被发送给新的订阅者。

When a server sends a PUBLISH to a client as a result of a subscription that already existed when the original PUBLISH arrived, the Retain flag should not be set, regardless of the Retain flag of the original PUBLISH. This allows a client to distinguish messages that are being received because they were retained and those that are being received "live".
这段部分没看懂，慢慢体会

restained messages应该在服务器重启后依旧存在（应该，有没有实现不清楚）

服务器何时删除retained message: 当服务器收到 某个topic上，0长payload, 并且设置了retain为1的消息时

*第一字节到此结束*

- Remaining Length:

剩余消息的字节数，包括了 `variable header`, `payload`

```php
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
