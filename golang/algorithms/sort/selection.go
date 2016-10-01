package sort

func SelectionSort(slice []int) {
	n := len(slice)

	for i := 0; i < n-1; i++ {
		minIndex := i

		for j := i; j < n; j++ {
			if slice[j] < slice[minIndex] {
				minIndex = j
			}
		}

		swap(slice, i, minIndex)
	}
}
