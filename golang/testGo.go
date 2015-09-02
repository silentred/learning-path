package main

import (
	"fmt"
	"sync"
	"time"
)

var counter int = 0

func Count(i int, lock *sync.Mutex) {
	lock.Lock()
	fmt.Println("B", i, counter)
	counter++
	fmt.Println("A", i, counter)
	lock.Unlock()
}

func main() {
	fmt.Println("starting...")
	lock := &sync.Mutex{}
	for i := 0; i < 9000; i++ {
		go Count(i, lock)
	}

	fmt.Println("ending...")

	time.Sleep(10 * time.Second)

	fmt.Println("over")
}
