package sort

func qsort(array []int, left, right int) {
	if left >= right {
		return
	}

	var i, j, tmp int
	tmp = array[left]
	i = left
	j = right

	for i < j {
		for array[j] >= tmp && i < j {
			j--
		}

		for array[i] <= tmp && i < j {
			i++
		}

		if i < j {
			swap(array, i, j)
		}
	}

	swap(array, i, left)

	qsort(array, left, i-1)
	qsort(array, i+1, right)
}
