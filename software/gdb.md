# gdb


set args /xxx/bin/php test.php

s: step into
n: step over
f: step out
c: continue
l: list
p: print
info break: 查看break信息
del #num : 删除第几个断点

```
$ gdb image

(gdb) b main.main
Breakpoint 1 at 0x2040: file /Users/jason/Desktop/projects/GOPATH/src/bmw/worker/image/main.go, line 14.

(gdb) bt
#0  main.main () at /Users/jason/Desktop/projects/GOPATH/src/bmw/worker/image/main.go:14

(gdb) p test
$1 = (struct bmw/lib.Test *) 0x13618 <runtime.typedmemmove+152>

(gdb) ptype test
type = struct bmw/lib.Test {
    struct string *Label;
    int32 *Type;
    struct []int64 Reps;
    struct bmw/lib.Test_OptionalGroup *Optionalgroup;
    struct []uint8 XXX_unrecognized;
} *

(gdb) p *test
$2 = {Label = <error reading variable: Cannot access memory at address 0xccccccc328c48350>, Type = 0x8a0250c8b4865, Reps =  []int64 = {
    <error reading variable>


```

# Delve

brew install go-delve/delve/delve

when uninstall:
$ sudo security delete-certificate -t -c dlv-cert /Library/Keychains/System.keychain

```
$ dlv debug

(dlv) b main.main
Breakpoint 2 set at 0x205f for main.main ./main.go:12

(dlv) c
> main.main() ./main.go:12 (hits goroutine(1):1 total:1)
     7:     "sync"
     8:     "sync/atomic"
     9: )
    10:
    11: func main() {
=>  12:     s := "123"
    13:     a := []int{1, 4, 6}
    14:     fmt.Println(s, a)
    15: }
    16:
    17: // func proto() {

(dlv) n
> main.main() ./main.go:14
     9: )
    10:
    11: func main() {
    12:     s := "123"
    13:     a := []int{1, 4, 6}
=>  14:     fmt.Println(s, a)
    15: }

(dlv) p a
[]int len: 3, cap: 3, [1,4,6]

(dlv) p &a
(*[]int)(0xc820049f10)

(dlv) locals
a = []int len: 3, cap: 3, [1,4,6]
s = "123"



```