package sort

import (
	"fmt"
	"testing"
)

func TestSelection(t *testing.T) {
	slice := []int{12, 35, 87, 26, 9, 28, 7}

	SelectionSort(slice)
	fmt.Println(slice)
}
