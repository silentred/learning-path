package sort

func InsertionSort(slice []int) {
	n := len(slice)

	// Version 1
	// sortedIndex := 0

	// for i := 0; i < n-1; i++ {
	// 	if slice[i] < slice[i+1] {
	// 		sortedIndex = i
	// 		continue
	// 	}
	// 	fmt.Println(slice)
	// 	_ = sortedIndex

	// 	sourceIndex := i + 1
	// 	sourceValue := slice[sourceIndex]
	// 	targetIndex := i

	// 	for targetIndex >= 0 && slice[targetIndex] > sourceValue {
	// 		targetIndex--
	// 	}
	// 	targetIndex++

	// 	fmt.Printf("i=%d sourceValue=%d targetIndex=%d \n", i, sourceValue, targetIndex)

	// 	for j := sourceIndex; j > targetIndex; j-- {
	// 		swap(slice, j, j-1)
	// 	}

	// 	slice[targetIndex] = sourceValue
	// }

	// Version 2
	for i := 1; i < n; i++ {
		srcVal := slice[i]
		j := i - 1

		for j >= 0 && slice[j] > srcVal {
			slice[j+1] = slice[j]
			j--
		}

		slice[j+1] = srcVal
	}
}
