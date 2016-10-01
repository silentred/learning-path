package sort

// BubbleSort sorts int slice
func BubbleSort(slice []int) {

	// Version 1
	// for i := len(slice) - 2; i > 0; i-- {
	// 	for j := 0; j <= i; j++ {
	// 		if slice[j] > slice[j+1] {
	// 			swap(slice, j, j+1)
	// 		}
	// 	}
	// }

	// Version 2

	n := len(slice)
	found := true

	for found {
		found = false
		for i := 0; i < n-1; i++ {
			if slice[i] > slice[i+1] {
				swap(slice, i, i+1)
				found = true
			}
		}
		n--
	}

}

func swap(slice []int, i, j int) {
	slice[i], slice[j] = slice[j], slice[i]
}
