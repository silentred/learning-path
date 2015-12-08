package main

import (
	"fmt"
)

func main() {

	var char1 rune = '赞'
	fmt.Printf("字符 %c 的unicode编码为 %U \n", char1, char1)

	var char2 string = "\\\""
	fmt.Printf("%%q 打印的字符为 %q, %%s 打印为 %s \n", char2, char2)

	var numbers4 = [...]int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
	slice5 := numbers4[4:]

	fmt.Println(slice5)

	newSlice := slice5

	/**
		Slice 内部有一个指向原生数组的指针，所以对slice元素的修改都是 by reference
	*/
	newSlice[0] = 99
	fmt.Println(slice5)
	fmt.Println(newSlice)

	newSlice2 := make([]int, len(newSlice))
	copy(newSlice2, newSlice)
	fmt.Println("newSlice2 is " , newSlice2)

	/**
	DELETE a[i]
	a = append(a[:i], a[i+1:]...)
	// or
	a = a[:i+copy(a[i:], a[i+1:])]
	*/
	i := 1
	length := copy(slice5[i:], slice5[i+1:])
	fmt.Println("copy returns " , length)
	fmt.Println("after copy , ", slice5)
	slice5 = slice5[:i+length]
	fmt.Println("after copy , ", slice5)




}
