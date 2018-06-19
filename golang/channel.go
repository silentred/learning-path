package main

import "fmt"

func Count(ch chan int) {
	fmt.Println("counting")
	ch <- 1
	// 因为ch满了，所以goroutine运行到这里阻塞，直到ch内容被拿出来后，才会继续运行下去
	fmt.Println("counting over")
}

func f(from string) {
	for i := 0; i < 3; i++ {
		fmt.Println(from, ":", i)
	}
}

func main() {
	// chs := make([]chan int, 10)
	// for i := 0; i < 10; i++ {
	//     chs[i] = make(chan int)
	//     //如果这里换成 chs[i] = make(chan int, 2)， "counting over"就会直接被打印，因为ch缓冲长度为2，没有满，goroutine可以继续执行
	//     go Count(chs[i])
	// }

	// for _, ch := range(chs) {
	//     fmt.Println(<-ch)
	//     //fmt.Println("read")
	// }

	/*ch := make(chan int, 1)
	  for{
	      select {
	          case ch <- 0:
	          case ch <- 1:
	      }
	      i := <-ch
	      fmt.Println("value recieved: ", i)
	  }*/

	/*f("direct")
	  go f("goroutine")
	  go func(msg string) {
	      fmt.Println(msg)
	  }("going")*/

	/*var input string
	fmt.Scanln(&input)*/

	var ch = make(chan int)

	go func() {
		num := <-ch
		// must print first
		fmt.Println(num)
	}()

	ch <- 123
	// must print after printing num
	fmt.Println("done")

}
