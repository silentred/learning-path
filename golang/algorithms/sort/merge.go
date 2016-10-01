package sort

func MergeSort(slice []int) {
	mergeSort(slice, 0, len(slice)-1)
}

func mergeSort(slice []int, start, end int) {
	if start < end {
		mid := (start + end) / 2
		mergeSort(slice, start, mid)
		mergeSort(slice, mid+1, end)
		merge(slice, start, mid, end)
	}
}

func merge(slice []int, start, mid, end int) {
	leftLen := mid - start + 1
	rightLen := end - mid

	leftArr := make([]int, leftLen)
	rightArr := make([]int, rightLen)

	// copy left part to leftArr
	copy(leftArr, slice[start:start+leftLen])
	// for i := 0; i < leftLen; i++ {
	// 	leftArr[i] = slice[start+i]
	// }

	copy(rightArr, slice[mid+1:mid+rightLen+1])
	// for j := 0; j < rightLen; j++ {
	// 	rightArr[j] = slice[mid+j+1]
	// }

	i, j := 0, 0
	k := start
	for i < leftLen && j < rightLen {
		if leftArr[i] <= rightArr[j] {
			slice[k] = leftArr[i]
			i++
		} else {
			slice[k] = rightArr[j]
			j++
		}
		k++
	}

	for i < leftLen {
		slice[k] = leftArr[i]
		i++
		k++
	}

	for i < rightLen {
		slice[k] = rightArr[j]
		j++
		k++
	}

}
