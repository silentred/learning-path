package sort

import (
	"fmt"
	"testing"
)

func TestInsert(t *testing.T) {
	slice := []int{12, 35, 87, 26, 9, 28, 7}

	InsertionSort(slice)
	fmt.Println(slice)
}
