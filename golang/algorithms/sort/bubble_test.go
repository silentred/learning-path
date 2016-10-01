package sort

import (
	"fmt"
	"testing"
)

func TestBubble(t *testing.T) {
	slice := []int{12, 35, 87, 26, 9, 28, 7}
	swap(slice, 1, 2)
	fmt.Println(slice)

	BubbleSort(slice)
	fmt.Println(slice)
}
