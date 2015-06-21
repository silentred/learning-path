package main

import "fmt"

func main() {

    var char1 rune  = '赞'
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
}
