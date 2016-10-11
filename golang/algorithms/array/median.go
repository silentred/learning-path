package array

func findMedian(a []int, b []int) float32 {
	n := len(a)
	bn := len(b)

	if n != bn {
		panic("a, b slice should have same length")
	}

	stopIndex := (2*n - 1) / 2

	i := 0
	var (
		curVal int
		aIndex int
		bIndex int

		stopVal     int
		stopNextVal int
	)

	for i <= stopIndex+1 {
		if a[aIndex] < b[bIndex] {
			curVal = a[aIndex]
			aIndex++
		} else {
			curVal = b[bIndex]
			bIndex++
		}

		if i == stopIndex {
			stopVal = curVal
		}

		if i == stopIndex+1 {
			stopNextVal = curVal
		}

		i++
	}

	return float32(stopVal+stopNextVal) / 2
}
