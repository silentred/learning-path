package sort

import (
	"fmt"
	"testing"
)

func TestHeap(t *testing.T) {
	slice := []int{12, 35, 87, 26, 9, 28, 7, 23, 45, 56, 67, 78, 89, 90, 14}

	HeapSort(slice)
	fmt.Println(slice)
}
