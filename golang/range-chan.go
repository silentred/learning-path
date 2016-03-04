package main

import (
	"fmt"
	"reflect"
	"time"
)

func main() {
	checkMethedSet()
	after()
	interval()
}

type I interface {
	Methed1()
	Method2()
}

func checkMethedSet() {
	var i *I
	elemType := reflect.TypeOf(i).Elem()
	n := elemType.NumMethod()
	for i := 0; i < n; i++ {
		fmt.Println(elemType.Method(i).Name)
	}
	// output "Method1, Method2"
}

func after() {
	// 可以用于检测 timeout
	c := make(chan int, 2)
	select {
	case m := <-c:
		fmt.Println(m)
	case <-time.After(2 * time.Second):
		fmt.Println("timed out")
	}
}

func interval() {
	// ## 每秒向 channel 中输入一个 Time
	ch := time.Tick(1 * time.Second)

	for now := range ch {
		fmt.Printf("%v \n", now)
	}
}
