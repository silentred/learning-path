package sort

import (
	"fmt"
	"testing"
)

func TestMerge(t *testing.T) {
	slice := []int{12, 35, 87, 26, 9, 28, 7, 23, 45, 56, 67, 78, 89, 90, 14}

	MergeSort(slice)
	fmt.Println(slice)
}

func TestRune(t *testing.T) {
	str := "你好"
	fmt.Println(len(str))
	mbStr := []rune(str)
	fmt.Println(len(mbStr))

	i := int64(-1)
	fmt.Printf("%b \n", uint64(i))
}
