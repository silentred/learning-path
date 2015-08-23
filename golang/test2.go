package main

import (
	"fmt"
	"time"
)

func main() {

	var char1 rune = '赞'
	fmt.Printf("字符 %c 的unicode编码为 %U \n", char1, char1)

	var char2 string = "\\\""
	fmt.Printf("%%q 打印的字符为 %q, %%s 打印为 %s \n", char2, char2)

	var numbers4 = [...]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	slice5 := numbers4[4:6:8]
	length := (2)
	capacity := (4)
	fmt.Printf("%v, %v\n", length == len(slice5), capacity == cap(slice5))
	fmt.Println(slice5)
	slice5 = slice5[:cap(slice5)]
	slice5 = append(slice5, 11, 12, 13)
	length = (7)
	fmt.Printf("%v\n", length == len(slice5))
	fmt.Println(slice5)
	slice6 := []int{0, 0, 0}
	copy(slice5, slice6)
	e2 := (0)
	e3 := (8)
	e4 := (11)
	fmt.Printf("%v, %v, %v\n", e2 == slice5[2], e3 == slice5[3], e4 == slice5[4])
	fmt.Println(slice5)

	jobs := make(chan int, 10)
	quit := make(chan int)

	// 一个 goroutine 从API获得数据，并保存到数据库。把图片数据保存到带缓存的jobs chan中。
	// 这个goroutine 可以被停止。 所以需要记录一个 next_url. next_url 也是一个 chan, 容量为1，
	// 取出一个url, 放入一个url.
	go func() {
		for {
			select {
			case <-quit:
				return
			default:
				jobs <- 33
				fmt.Println("getting img from api")
			}
			time.Sleep(1 * time.Second)
		}
	}()

	// 下载 goroutine, 负责从jobs中取出job, 进行下载操作。
	// 用 管道模式 比较好? 第一个 routine 返回一个buffered jobs chan, 第二个 routine 接受一个只读的 jobs, 从其中读取job
	go func() {
		var job int
		for {
			job = <-jobs
			fmt.Println("doing the job: " + string(job))
		}
	}()

	time.Sleep(5 * time.Second)
	quit <- 1
	time.Sleep(1 * time.Second)
	fmt.Println("closing the jobs and quit")
	close(jobs)
	close(quit)

}
