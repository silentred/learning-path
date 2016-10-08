package array

func majority(slice []int) int {
	var candicate int
	var count int
	n := len(slice)

	for i := 0; i < n; i++ {
		if count == 0 {
			candicate = slice[i]
			count = 1
			continue
		} else {
			if candicate == slice[i] {
				count++
			} else {
				count--
			}
		}
	}

	if count == 0 {
		return -1
	}

	count = 0
	for i := 0; i < n; i++ {
		if candicate == slice[i] {
			count++
		}
	}

	if count > n/2 {
		return candicate
	}

	return -1
}
