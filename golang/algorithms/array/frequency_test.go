package array

import (
	"fmt"
	"testing"
)

func TestFrequency(t *testing.T) {
	slice := []int{2, 3, 3, 2, 5}

	slice = count(slice)

	for i := 0; i < len(slice); i++ {
		fmt.Printf("num %d shows %d times \n", i+1, slice[i])
	}

}

func TestBSearch(t *testing.T) {
	slice := []int{1, 2, 3, 4, 5, 6}
	res := bSearch(slice, 6)
	fmt.Println(res)
}

func TestFib(t *testing.T) {
	fmt.Println(fib(10))
}
