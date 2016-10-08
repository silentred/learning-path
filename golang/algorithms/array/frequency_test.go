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
