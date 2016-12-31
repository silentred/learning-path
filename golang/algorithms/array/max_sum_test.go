package array

import (
	"fmt"
	"testing"
)

func TestMaxSum(t *testing.T) {
	s := []int{2, -9, 5, 1, -4, 6, 0, -7, 8}
	//s := []int{-9, -1, -4, -6, -7, -8}
	max := maxSum(s)
	fmt.Println(max)
}

func TestNextGreater(t *testing.T) {
	s := []int{98, 23, 54, 12, 20, 7, 27}
	nextGreater(s)
}

func TestRoate(t *testing.T) {
	s := []int{1, 2, 3, 4, 5, 6}
	//reverse(s, 0, len(s)-1)
	rotate(s, 2)
	fmt.Println(s)
}

func TestMajority(t *testing.T) {
	s := []int{2, 6, 2, 2, 6, 2, 2, 8, 2, 1}
	//s := []int{1, 7, 8, 2, 6, 8, 1, 3, 2, 8}
	fmt.Println(majority(s))
}

func TestReverse(t *testing.T) {
	s := []int{2, 6, 1, 3}

	var start int
	var end = len(s) - 1
	for start < end {
		s[start], s[end] = s[end], s[start]
		start++
		end--
	}

	fmt.Println(s)
}
