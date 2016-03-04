package main

import (
	"fmt"
	"log"
	"sync"
)

var counter int = 0

func Count(i int, lock *sync.Mutex) {
	lock.Lock()
	fmt.Println("B", i, counter)
	counter++
	fmt.Println("A", i, counter)
	lock.Unlock()
}

func OutFunc() (i int, err error) {
	defer func() {
		if e := recover(); e != nil {
			err = fmt.Errorf("%v", e)
		}
	}()
	i = 1
	panic("do panic in OutFunc..")
	return i, err
}

func main() {
	_, err := OutFunc()
	if err != nil {
		log.Printf("error is : %v", err)
	}
	fmt.Printf("End of main")

	data := []int{0, 1, 2, 3, 4}
	s1 := data[:2]
	fmt.Printf("data ptr is %p, s1 ptr is %p", &data, &s1)
	s2 := append(s1, 100, 200)
	fmt.Println("\n", data)
	fmt.Println(s1)
	fmt.Println(s2)
	fmt.Printf("data ptr is %p, s1 ptr is %p, s2 ptr is %p \n", &data, &s1, &s2)

	var pool *sync.Pool
	pool = new(sync.Pool)
	pool.New = func() interface{} {
		return 1
	}
	//pool.Put(1)
	i := pool.Get()
	if i == nil {
		fmt.Println("pool.Get is non-block function. nil could be returned. not cool")
	} else {
		fmt.Println("number is ", i)
	}

}
