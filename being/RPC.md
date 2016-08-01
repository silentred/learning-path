# RPC

协议仿照 json-rpc
序列化使用 msgpack

```go
type Rquest struct {
	Version uint16 `msg:"v"`
	Method string `msg:"m"`
	Params *msgp.Raw `msg:"p"`
	Id  uint64 `msg:"id"`
}

type Response struct {
	Version uint16
	Result interface{}
	Error string
	Id uint64
}

```

reqest 结构:

```json
{
	v: 1,
	m: "Object.Method",
	p: {arg1: 1, arg2: "test"},
	id: 2
}

response 结构:
{
	v: 1,
	r: {...},
	e: null,
	id: 2
}
```

