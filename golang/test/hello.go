package main

import "fmt"

func main() {
	fmt.Printf("hello, world\n")
	obj := get()
	str, _ := obj.([]byte)
	fmt.Printf("%#v %t \n", str, str == nil)
}

func get() (obj interface{}) {
	return nil
}
