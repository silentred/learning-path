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
