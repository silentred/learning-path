package main

import "fmt"

// #cgo CFLAGS: -I.
// #cgo LDFLAGS: -L. -lgb
// #include <add.h>
import "C"

func main() {
	fmt.Println("invoking c lib")
	fmt.Println("Done ", C.add(1))
}

/**
导出 Go 函数给 C 调用
**/
//export myprint
func myprint(i C.int) {
	fmt.Printf("my print: %d \n", i)
}
