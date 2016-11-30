package sort

import (
	"fmt"
	"testing"
)

func TestQuick(t *testing.T) {
	slice := []int{12, 35, 12, 21, 14, 14, 87, 26, 9, 28, 7}

	qsort(slice, 0, len(slice)-1)
	fmt.Println(slice)
}
