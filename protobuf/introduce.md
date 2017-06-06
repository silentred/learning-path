# Introduce

```
syntax = "proto3";

message SearchRequest {
  string query = 1;
  int32 page_number = 2;
  int32 result_per_page = 3;
}
```

## Number Tag

最后的数字是字段的唯一标识(包含了标识数字和字段类型)，1-15 占用1个字节，16-2047 占用2字节。所以 1-15 应该用来标记最常用的字段。
19000 - 19999 是被保留的，不能使用。

## 单复数

singular: 单数, 默认是单数，不用加关键词。
repeated: 复数的关键词。

## 保留字段

```
message Foo {
  reserved 2, 15, 9 to 11;
  reserved "foo", "bar";
}
```
如果想删除字段，但是为了兼容，想保留某些字段，不让别人使用，可以用关键词 reserved

## 标量默认值

strings: ""
bytes: []
bools: false
numerics: 0
enums: 第一个值

## 枚举 enumeration

```
enum EnumAllowingAlias {
  UNKNOWN = 0;
  STARTED = 1;
}
```
枚举第一个值必须为0. 

可以使用别名, 使用 `option allow_alias=true;` ，例如：
```
enum EnumAllowingAlias {
  option allow_alias = true;
  UNKNOWN = 0;
  STARTED = 1;
  RUNNING = 1; // valid only when set allow_alias=true
}
```

## 使用Message类型作为字段

```
message SearchResponse {
  repeated Result results = 1;
}

message Result {
  string url = 1;
  string title = 2;
  repeated string snippets = 3;
}
```

### 导入定义

如果 Result 定义在别的 .proto 文件中，那么可以在文件顶部写 `import "myproject/other_protos.proto";`

关键词 `import public` 的作用是：可以间接导入。例如：
```
// new.proto
// all the real definitions

// old.proto
import public "new.proto"

// client.proto
import "old.proto"
这个文件中能直接使用 new.proto 中的定义类型，这就是 import public 的作用.

```

使用 compiler 时，注意加上 `-I` 参数，指定.proto文件的根目录, compiler用于解析 import 指令。

## Nested Types

```
message SearchResponse {
  message Result {
    string url = 1;
    string title = 2;
    repeated string snippets = 3;
  }
  repeated Result results = 1;
}


message SomeOtherMessage {
  SearchResponse.Result result = 1;
}
```

## 更新 Message Type

- 不要修改 numeric tag
- 如果只是添加字段，那么新类型和旧类型是兼容的，只是新字段有默认值。兼容是指： 旧的binary 可以解析为 新类型，新字段为默认值； 新的binary可以解析为旧类型，新字段被忽略.
- 字段可以删除，使用 reserved, 或者修改字段名称，例如加上 "OBSOLETE_" 前缀
- int32, uint32, int64, uint64, bool 是互相兼容的。
- sint32, sint64, 互相兼容，但不兼容其他数字类型
- string, bytes 互相兼容，只要 bytes 是 UTF-8
- 嵌入消息 和 bytes 兼容
- fixed32 与 sfixed32, fixed64, sfixed64 兼容
- enum 与 int32, uint32, int64, uint64 兼容


## Any

Any 可以被 pack(), unpack()
message Any {
  bytes data // 序列化
  string url // 标识, default is type.googleapis.com/packagename.messagename
}

## Oneof

有oneof关键词 的 fields 共享内存，最多只能有一个被设定，类似 c 的 union 类型

```
message SampleMessage {
  oneof test_oneof {
    string name = 4;
    SubMessage sub_message = 9;
  }
}
```
oneof 的字段内不能使用 repeated.
oneof 有向后兼容的问题，还挺多.

## Maps

`map<key_type, value_type> map_field = N;`

key_type 可以为除了 float, bytes的标量； value_type 可以为任意类型

- map 不能为 repeated
- map 中，item 无顺序
- map中如果key重复，最后一个key会覆盖前面的。

proto3 支持map， 对于之前的版本，可以使用:

```
message MapFieldEntry {
  key_type key = 1;
  value_type value = 2;
}

repeated MapFieldEntry map_field = N;
```

## Packages

```
package foo.bar;
message Open { ... }
```

对于Go， package会用作 go package name。 也可以用 `option go_package` 显式指定.

## Services

## JSON mapping

## options

## Generating Code

`protoc -I=IMPORT_PATH --go_out=DEST_DIR path/to/file.proto`

## grpc
`protoc -I=IMPORT_PATH --go_out=plugins=grpc:DEST_DIR path/to/file.proto`





